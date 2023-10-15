from flask import Flask, session, render_template, request, abort, redirect, url_for, flash
from database import add_user_to_database
import secret_key
import json

app = Flask(__name__)

app.secret_key = secret_key.secret_key

with open("/home/david/Files/anestesioMack2/users_dict.json", 'r') as f:
    users = json.load(f)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        crm = request.form.get("crm")
        password = request.form.get("password")

        if users.get(crm) == password:
            session["crm"] = crm
            return redirect(url_for("protected"))
        flash("CRM ou senha incorretos.")

    return render_template("home.html")


@app.route("/protected")
def protected():
    if not session.get("crm"):
        abort(401)
    return render_template("protected.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phoneNum")
        email = request.form.get("email")
        crm = request.form.get("crm")
        rqe = request.form.get("rqe")
        password = request.form.get("password")

        add_user_to_database(crm, name, phone, email, rqe)
        users[crm] = password

        with open("/home/david/Files/anestesioMack2/users_dict.json", 'w') as g:
            json.dump(users, g)

        flash("Signup completo!")
        return redirect(url_for("home"))

    return render_template("signup.html")
