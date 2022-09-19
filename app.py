from http.client import responses
from urllib import response
from flask import Flask, redirect, render_template, request, flash, make_response, jsonify, url_for
from flask_bootstrap import Bootstrap
from flask import session as Fsession
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField, SelectField, BooleanField
from wtforms.validators import DataRequired, InputRequired
from sasctl import Session, current_session, get, post, put, delete
import json
from random import randrange




app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
bootstrap = Bootstrap(app)

class SettingForms(FlaskForm):
    viya_url = StringField('What`s your host', validators=[DataRequired()])
    username = StringField('What`s your username for SAS`?',
                           validators=[DataRequired()])
    password = PasswordField('Provide Pass', validators=[InputRequired()])
    publishedDecision = StringField(
        'Decision Name ', validators=[DataRequired()])


class Decisionform(FlaskForm):
    job = SelectField('Please select your job', choices=[
                      ('Sales'), ('Manager'), ('Office'), ('Executive Professor'), ('Self'), ('Other')])
    loan = IntegerField('How much Loan you need ?')
    mortdue = IntegerField(
        'Please provide your amount due on existing mortgage ')
    delinq = FloatField(' Number of delinquent credit lines ')
    derog = IntegerField(' Number of major derogatory reports ')
    clage = IntegerField('Age of your oldest credit line in months?')
    ninq = IntegerField('Number of your recent credit inquiries ')
    clno = IntegerField('Number of your credit lines')
    yoj = IntegerField(' Years at present job ')
    reason = SelectField('Why do you need credit?', choices=[
                         ('Debt Consolidation'), ('Home Improvement'), ('Other')])
    income = IntegerField('What`s your income ')
    value = IntegerField('Your current value of property')
    currentDebt = IntegerField('What`s your current debt ?')
    submit = SubmitField('Submit')
    average_active = BooleanField(
        'Would you like to fill with average values ?', default=False)


@app.route('/')
def home_page():
    return render_template('user.html')


# @app.route('/settings', methods=['GET', 'POST'])
# def form():
#     global publishedDecision
#     form = SettingForms()
#     publishedDecision = form.publishedDecision.data

#     if request.method == 'POST' and form.validate_on_submit():
#         sess = Session(form.viya_url.data, form.username.data,
#                        form.password.data, verify_ssl=False)
#         current_session(sess)
#         Fsession['session'] = 'SAS'
#         return redirect('/decision')
#     else:
#         redirect('404.html')
#     return render_template('form.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/decision-average', methods=['GET', 'POST'])
def averageDecision():
    averageDecisionForm = Decisionform()
    averageDecisionForm.loan.data = str(randrange(1800,1900))
    averageDecisionForm.mortdue.data = str(randrange(72000,73769))
    averageDecisionForm.reason.data = "Reason"
    averageDecisionForm.yoj.data = str(randrange(5,10))
    averageDecisionForm.delinq.data = "0"
    averageDecisionForm.derog.data = "0"
    averageDecisionForm.clage.data = str(randrange(170,190))
    averageDecisionForm.delinq.data = "0"
    averageDecisionForm.value.data = str(randrange(101500,102000))
    averageDecisionForm.clno.data = str(randrange(18,22))
    averageDecisionForm.ninq.data = "1"
    averageDecisionForm.income.data = str(randrange(63000,67000))
    averageDecisionForm.currentDebt.data = str(randrange(1900,2100))
    averageDecisionForm.job.data = "Self"
    averageDecisionForm.reason.data = "Home Improvement"

    avg_req = {
        "inputs": [
            {"name": "JOB_",
                     "value": averageDecisionForm.job.data},
            {"name": "LOAN_",
                     "value": averageDecisionForm.loan.data},
            {"name": "MORTDUE_",
                     "value": averageDecisionForm.mortdue.data},
            {"name": "REASON_",
                     "value": "HomeImp"},
            {"name": "YOJ_",
                     "value": averageDecisionForm.yoj.data},
            {"name": "DEBTINC_",
                     "value": "33"},
            {"name": "DELINQ_",
                     "value": averageDecisionForm.delinq.data},
            {"name": "DEROG_",
                     "value": averageDecisionForm.derog.data},
            {"name": "CLAGE_",
                     "value": averageDecisionForm.clage.data},
            {"name": "NINQ_",
                     "value": averageDecisionForm.delinq.data},
            {"name": "VALUE_",
                     "value": averageDecisionForm.value.data},
            {"name": "CLNO_",
                     "value": averageDecisionForm.clno.data}
        ]}
    if request.method == 'POST' and averageDecisionForm.validate_on_submit:
        flash('you are about to submit inputs are you sure')
    #make_call(avg_req)

    return render_template('averageInputs.html', form=averageDecisionForm)


@app.route('/odd-input',methods=['GET','POST'])
def oddInput():
    var1 = 0
    if var1 == 0 and request.method == 'GET' :
        flash('works')
        return redirect(url_for("scoreDecision"))
    else: flash('some random message')
    return render_template('warning.html')

def make_call(body):
    contentType = "application/vnd.sas.microanalytic.module.step.input+json"
    masExecutionResponse = post(f"microanalyticScore/modules/{publishedDecision}/steps/execute",
                headers={"Content-Type": contentType}, data=json.dumps(body))
    if masExecutionResponse.get('executionState') == 'completed':
                resp = {d['name']: d['value']
                        for d in dict(masExecutionResponse)['outputs'][1:18]}
                return make_response(jsonify(resp), 200)
    elif masExecutionResponse.get('httpStatusCode') == 400:
            return make_response(masExecutionResponse.get('message'))
    else: return(masExecutionResponse.get('httpStatusCode'))



@app.route('/decision', methods=['GET', 'POST'])
def scoreDecision():
    formDecision = Decisionform()
    if formDecision.average_active.data == True and request.method == 'POST':
        return redirect(url_for('ConfirmAction'))

    res = {
        "inputs": [
            {"name": "JOB_",
                     "value": ''},
            {"name": "LOAN_",
                     "value": formDecision.loan.data},
            {"name": "MORTDUE_",
                     "value": formDecision.mortdue.data},
            {"name": "REASON_",
                     "value": formDecision.reason.data},
            {"name": "YOJ_",
                     "value": formDecision.yoj.data},
            {"name": "DEBTINC_",
                     "value": ''},
            {"name": "DELINQ_",
                     "value": formDecision.delinq.data},
            {"name": "DEROG_",
                     "value": formDecision.derog.data},
            {"name": "CLAGE_",
                     "value": formDecision.clage.data},
            {"name": "NINQ_",
                     "value": formDecision.delinq.data},
            {"name": "VALUE_",
                     "value": formDecision.value.data},
            {"name": "CLNO_",
                     "value": formDecision.clno.data}
        ]}
    if request.method == 'POST' and formDecision.validate_on_submit:
        debtinc = .3
        # if formDecision.reason.data == 'Debt Consolidation':
        #     res['inputs'][3] = {'name': 'REASON_', 'value': 'DebtCon'}
        # elif formDecision.reason.data == 'Home Improvement':
        #     res['inputs'][3] = {'name': 'REASON_', 'value': 'HomeImp'}
        # else:
        #     res['inputs'][3] = {'name': 'REASON_', 'value': 'Other'}
        # res['inputs'][5] = {'name': 'DEBTINC_', 'value': debtinc}
        if formDecision.job.data == 'Sales' and 41000 <= formDecision.income.data <= 89000 and debtinc < .5:
            res['inputs'][0] = {'name': 'JOB_', 'value': formDecision.job.data}
            flash('anananana')
            #return redirect(url_for('ConfirmAction'))
            make_call(res)
        elif formDecision.job.data == 'Sales' and formDecision.income.data < 40000:
            flash('Your income and debt looks odd are you sure you want to continue ? ')
            make_call(res)

        elif formDecision.job.data == 'Manager' and 44000 <= formDecision.income.data <= 107000 and debtinc < .5:
            res['inputs'][0] = {'name': 'JOB_', 'value': 'Mgr'}
            flash('Your income and debt looks odd are you sure you want to continue ? ')
            make_call(res)
        elif formDecision.job.data == 'Manager' and formDecision.income.data < 40000:
            flash('Your income and debt looks odd are you sure you want to continue ? ')
            make_call(res)
        elif formDecision.job.data in ['Office', 'Other'] and 18000 <= formDecision.income.data <= 71000 and debtinc < .5:
            res['inputs'][0] = {'name': 'JOB_', 'value': formDecision.job.data}
            flash('Your income and debt looks odd are you sure you want to continue ? ')
            make_call(res)
        elif formDecision.job.data == 'Executive Professor' and 69000 <= formDecision.income.data <= 200000 and debtinc < .5:
            res['inputs'][0] = {'name': 'JOB_', 'value': 'ProfExe'}
            flash('Your income and debt looks odd are you sure you want to continue ? ')
            make_call(res)
        elif formDecision.job.data == 'Self' and 30000 <= formDecision.income.data <= 350000 and debtinc < .5:
            res['inputs'][0] = {'name': 'JOB_', 'value': formDecision.job.data}
            flash('Your income and debt looks odd are you sure you want to continue ? ')
            make_call(res)
        elif debtinc > .5:
            flash('Your income and debt looks odd are you sure you want to continue ? ')
            return redirect(url_for('odd-input'))
        # else:
        #     return render_template('404.html')
    return render_template('inputs.html', form=formDecision)

@app.route('/ConfirmationAverage',methods=['GET','POST'])
def ConfirmAction():
    #flash('We will fill the form with average values, would you like to proceed?')
    if request.method == 'POST':
        return redirect(url_for('averageDecision'))
    return render_template('confirmAverage.html')

if __name__ == "__main__":
    app.run(debug=True)
