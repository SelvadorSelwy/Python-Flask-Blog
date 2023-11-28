from flask import Blueprint, render_template, redirect, url_for,request, flash
from . import db 
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
# from dotenv import load_dotenv
# from flask_socketio import SocketIO



auth= Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email= request.form.get("email")
        password= request.form.get("password")
        user= User.query.filter_by(email= email).first()
        if user:
            if check_password_hash(user.password , password):
                flash("Logged in..", category= "success")
                login_user(user, remember= True)
                return redirect(url_for("views.index"))
            else:
                flash("Incorrect Password", category= "error")

        else:
            flash("This email addrress is not exist", category="danger")

    return render_template("login.html", user= current_user, logs= "logins")



@auth.route("/sign-up" , methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html", user= current_user)
    else:
        username= request.form.get("username")
        email= request.form.get("email")
        password= request.form.get("password")
        confirm_pw= request.form.get("confirmPw")
        if len(username)< 2:
            flash(message="The username is too short , Try again with true name!", category="error")

        elif User.query.filter_by(username=username).first():
            flash("This username is already exist, choose another name.", category="error")

        elif User.query.filter_by(email= email).first():
            flash("This email is alreay exist, enter another email.", category="error")


        
        elif len(password) < 6:
            flash("Password must be at least 6 character!", category= "error")
        
        elif confirm_pw != password:
            flash("The password dose not match , Try again!")

        else:
            # new_user= User(username= username, email=email, password= generate_password_hash(password, method='sha256'))
            new_user= User(username= username, email=email, password= generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash("User Created..", category="success")
            login_user(new_user, remember= True)
            return redirect(url_for("views.index"))
 
    return render_template("signup.html", user=current_user)
            

@login_required
@auth.route("/log-out")
def log_out():
    logout_user()
    return redirect(url_for("views.main" ))


# -----------------------------------------
# from passlib.hash import sha256_crypt

# password = "test"
# passwordata = sha256_crypt.encrypt(password)

# if sha256_crypt.verify(password, passwordata):
#     print("OK")