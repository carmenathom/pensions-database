from flask import Blueprint, render_template, request, redirect, session, url_for
from models import create_user, validate_login

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        create_user(
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"],
            role=request.form["role"],     
            name=request.form["name"]
        )
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = validate_login(
            username=request.form["username"],
            password=request.form["password"]
        )

        if user:
            session["user_id"] = user['user_id']
            session["username"] = user['username']
            session["role"] = user['role']
            return redirect(url_for("index"))
        else:
            return "Invalid credentials" 
    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
