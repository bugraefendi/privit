from flask import Flask, redirect, render_template,request,flash,url_for,make_response,jsonify
from flask_bootstrap import Bootstrap
from flask import session as Fsession
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,IntegerField,FloatField
from wtforms.validators import DataRequired,InputRequired
from sasctl import Session, current_session, get, post, put, delete
import json



app = Flask(__name__)
app.secret_key = 'hardstring to guesss'
bootstrap = Bootstrap(app)

class SettingForms(FlaskForm):
    viya_url = StringField('What`s your host', validators=[DataRequired()])
    username = StringField('What`s your username for SAS`?',validators=[DataRequired()] )
    password = PasswordField('Provide Pass',validators=[InputRequired()])
    publishedDecision = StringField('Decision Name ',validators=[DataRequired()])
    
class Decisionform(FlaskForm):
    job = StringField('Please provide your job')
    loan = IntegerField('How much Loan you need ?')
    mortdue = IntegerField('Please provide your amount due on existing mortgage ')
    delinq = FloatField(' Number of delinquent credit lines ')
    derog =IntegerField(' Number of major derogatory reports ')
    clage = IntegerField('Age of your oldest credit line in months')
    ninq = IntegerField('Number of your recent credit inquiries ')
    clno =IntegerField('Number of your credit lines')
    yoj = IntegerField(' Years at present job ')
    reason = StringField('Why do you need credit')
    income = IntegerField('What`s your income ')
    value = IntegerField('Your current value of property')
    currentDebt = IntegerField('What`s your current debt ?')
    submit = SubmitField('Submit')



@app.route('/')
def home_page():
    return render_template('user.html')

@app.route('/settings',methods=['GET','POST'])
def form():
    global publishedDecision
    form = SettingForms()
    publishedDecision = form.publishedDecision.data

    if request.method == 'POST' and form.validate_on_submit:
        try:
            sess = Session(form.viya_url.data, form.username.data,form.password.data, verify_ssl=False)
            current_session(sess)
            Fsession['session'] = 'SAS'
            return redirect('/decision')
        except: redirect('404.html')
    else: redirect('404.html')
    return render_template('form.html',form=form)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404




@app.route('/decision',methods=['GET','POST'])
def scoreDecision():
    formDecision = Decisionform()
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
    contentType = "application/vnd.sas.microanalytic.module.step.input+json"
    publishedDecision
    if request.method == 'POST' and formDecision.validate_on_submit and 'session' in Fsession:
        debtinc = formDecision.currentDebt.data / formDecision.income.data
        res['inputs'][5] = {'name': 'DEBTINC_', 'value': debtinc}
        if formDecision.job.data.upper() == 'SALES' and 41000 <= formDecision.income.data <= 89000:
            res['inputs'][0] = {'name': 'JOB_', 'value': formDecision.job.data.upper()}
            masExecutionResponse = post(f"microanalyticScore/modules/{publishedDecision}/steps/execute",
                                        headers={"Content-Type": contentType}, data=json.dumps(res))
            if masExecutionResponse.get('executionState') == 'completed':
                resp = {d['name']: d['value']
                        for d in dict(masExecutionResponse)['outputs'][1:18]}
                return make_response(jsonify(resp), 200)
        elif formDecision.job.data.upper() == 'SALES' and formDecision.income.data < 40000:
            print('Your Income and job does not match')
            
        elif formDecision.job.data.upper() in ['MGR','MANAGER'] and 44000 <= formDecision.income.data <= 107000:
            res['inputs'][0] = {'name': 'JOB_', 'value': formDecision.job.data}
            masExecutionResponse = post(f"microanalyticScore/modules/{publishedDecision}/steps/execute",
                                        headers={"Content-Type": contentType}, data=json.dumps(res))
            if masExecutionResponse.get('executionState') == 'completed':
                resp = {d['name']: d['value']
                        for d in dict(masExecutionResponse)['outputs'][1:18]}
                return make_response(jsonify(resp), 200)
        elif formDecision.job.data.upper() in ['MGR','MANAGER'] and formDecision.income.data < 40000:
            print('Your Income and job does not match')
        elif formDecision.job.data in ['Office', 'Other'] and 18000 <= formDecision.income.data <= 71000:
            res['inputs'][0] = {'name': 'JOB_', 'value': formDecision.job.data}
            masExecutionResponse = post(f"microanalyticScore/modules/{publishedDecision}/steps/execute",
                                        headers={"Content-Type": contentType}, data=json.dumps(res))
            if masExecutionResponse.get('executionState') == 'completed':
                resp = {d['name']: d['value']
                        for d in dict(masExecutionResponse)['outputs'][1:18]}
                return make_response(jsonify(resp), 200)
        elif debtinc > .5:
            print('Your Debt to Income is too high')
            return ('404')
        else: print('General Error page  ')
    return render_template('inputs.html', form=formDecision)
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

