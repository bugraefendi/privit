from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField,  SelectField, BooleanField
from wtforms.validators import DataRequired, InputRequired



class SettingForms(FlaskForm):
    viya_url = StringField('Host name', validators=[DataRequired()])
    cas_host = StringField('What`s your CAS Host ?')
    username = StringField('SAS username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    publishedDecision = StringField(
        'Decision Name', validators=[DataRequired()])


class Decisionform(FlaskForm):
    job = SelectField('Select your job', choices=[
                      ('Sales'), ('Manager'), ('Office'), ('Executive Professor'), ('Self'), ('Other')],default="")
    loan = IntegerField('How much Loan you need?')
    mortdue = IntegerField('Amount due on existing mortgage')
    delinq = IntegerField('No. of delinquent credit lines')
    derog = IntegerField('No. of major derogatory reports')
    clage = IntegerField('Age of  the oldest credit line (months)')
    ninq = IntegerField('No. of recent credit inquiries')
    clno = IntegerField('No. of credit lines')
    yoj = IntegerField('Years at present job')
    reason = SelectField('Why do you need credit?', choices=[
                         ('Debt Consolidation'), ('Home Improvement'), ('Other')])
    income = IntegerField('Current Income', validators=[DataRequired()])
    value = IntegerField('Current value of property')
    currentDebt = IntegerField('Current debt', validators=[DataRequired()])
    submit = SubmitField('Submit')
    average_active = BooleanField('Fill with average values', default=False)