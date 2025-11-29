import os
from auth import auth
from db import get_db
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") 
app.register_blueprint(auth)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    session['user'] = "example_user"
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))

if __name__ == '__main__': 
    app.run(debug = True)