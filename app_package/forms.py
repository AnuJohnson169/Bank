from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import DataRequired, EqualTo
from app_package.models import User

class LoginForm(FlaskForm):
    username=StringField("Username: ",validators=[DataRequired()])
    password=PasswordField("Password: ",validators=[DataRequired()])
    remember_me=BooleanField("Remember Me")
    submit=SubmitField("Sign in")
              
class AddAccountHolderForm(FlaskForm):
    accno=IntegerField("Account Number: ",validators=[DataRequired()])
    accname=StringField("Account Holder Name: ",validators=[DataRequired()])
    acctype=StringField("Account Type: ",validators=[DataRequired()])
    bal=IntegerField("Balance Amount: ",validators=[DataRequired()])
    submit=SubmitField("Create new account")
    
class CloseAccountForm(FlaskForm):
    accno=IntegerField("account no to be deleted: ", validators=[DataRequired()])    
    submit=SubmitField("Close account")
    
class DeleteForm(FlaskForm):
    accno=IntegerField("confirm account no: ",validators=[DataRequired()])
    submit=SubmitField("Delete")
        
class WithdrawalForm(FlaskForm):
    accno=IntegerField("Enter Account no: ",validators=[DataRequired()])
    widamt=IntegerField("Enter Withdraw Amount : ",validators=[DataRequired()])
    submit=SubmitField("Withdraw")
    
class DepositForm(FlaskForm):
    accno=IntegerField("Enter Account no: ",validators=[DataRequired()])
    depamt=IntegerField("Enter Deposit Amount : ",validators=[DataRequired()])
    submit=SubmitField("Deposit")    
    
class BalanceEnquiryForm(FlaskForm):
    accno=IntegerField("Enter Account no: ",validators=[DataRequired()])
    submit=SubmitField("Check balance")        
    
    
    
        
