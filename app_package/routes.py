from flask import render_template, flash, redirect, url_for
from app_package import app, db, mongo
from flask_login import current_user, login_user, logout_user, login_required
from app_package.forms import LoginForm, AddAccountHolderForm, CloseAccountForm, WithdrawalForm, DepositForm, BalanceEnquiryForm, DeleteForm
from app_package.models import User

bank_id=0
@app.route("/",methods=["GET","POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid user")
                return redirect(url_for("index"))
            else:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("menu"))
        else:
            return render_template("login.html",form=form)
            
@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html")        
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))         
    
@app.route("/add_account",methods=["GET","POST"])    
@login_required
def add_account():
    global bank_id
    form=AddAccountHolderForm()
    if form.validate_on_submit():
        fields=["_id","accno","accname","acctype","bal"]
        bank_id+=1
        values=[bank_id,form.accno.data,form.accname.data,form.acctype.data,form.bal.data]
        bank=dict(zip(fields,values))
        bank_col=mongo.db.bank
        tmp=bank_col.insert_one(bank)
        if tmp.inserted_id==bank_id:
            flash("Account created successfully")
            return redirect(url_for("menu"))
        else:
            flash("error adding account")
            return redirect(url_for("logout"))
    else:         
        return render_template("add_account.html",form=form)               
        
@app.route("/close_account",methods=["GET","POST"])
@login_required
def close_account():
    form=CloseAccountForm()
    dform=DeleteForm()
    if form.validate_on_submit():
        bank_col=mongo.db.bank
        query={"accno":form.accno.data}
        bank=bank_col.find_one(query)
        return render_template("confirm_account.html",dform=dform,bank=bank)
    else:
        return render_template("close_account.html",form=form)
        
@app.route("/confirm_account",methods=["GET","POST"])   
def confirm():
    dform=DeleteForm()
    bank_col=mongo.db.bank
    query={"accno":dform.accno.data}
    bank_col.delete_one(query)
    flash("account deleted")
    return redirect(url_for("menu"))
     
@app.route("/withdraw_amount",methods=["GET","POST"])
@login_required
def withdraw_amount():
    form=WithdrawalForm()         
    if form.validate_on_submit():
        values=dict()
        if form.accno.data!="":values["accno"]=form.accno.data
        query={"accno":form.accno.data}
        bank_col=mongo.db.bank
        b=bank_col.find_one(query)
        bal=b["bal"]
        acctype=b["acctype"]
        new_bal=bal-form.widamt.data
        if acctype=="priority" and new_bal<50000 or acctype=="ordinary" and new_bal<10000:
            flash("Low balance")
            return redirect(url_for("menu"))
        else:
            new_data={"$set":{"bal":new_bal}}
            bank_col.update_one(query,new_data)
            flash("Amount debited successfully")
            return redirect(url_for("menu"))     
    else:
        return render_template("withdraw_amount.html",form=form)
        
@app.route("/deposit_amount",methods=["GET","POST"])
@login_required
def deposit_amount():
    form=DepositForm()         
    if form.validate_on_submit():
        values=dict()
        if form.accno.data!="":values["accno"]=form.accno.data
        query={"accno":form.accno.data}
        bank_col=mongo.db.bank
        b=bank_col.find_one(query)
        bal=b["bal"] 
        values["bal"]=bal+form.depamt.data
        new_data={"$set":values}
        bank_col.update_one(query,new_data)
        flash("Amount deposited successfully")
        return redirect(url_for("menu"))
    else:
        return render_template("deposit_amount.html",form=form)        

@app.route("/balance_enquiry",methods=["GET","POST"])
@login_required
def balance_enquiry():
    form=BalanceEnquiryForm()
    if form.validate_on_submit():
        bank_col=mongo.db.bank
        query={"accno":form.accno.data}
        bank=bank_col.find(query)
        return render_template("display_balance.html",bank=bank) 
    else:    
        return render_template("balance_enquiry.html",form=form) 
        

            
@app.route("/display_balance",methods=["GET","POST"])
@login_required
def display_balance():
    bank_col=mongo.db.bank
    bank=bank_col.find()
    return render_template("display_balance.html",bank=bank) 
        
    
