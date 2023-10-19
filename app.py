from flask import Flask, session, render_template, request, abort, redirect, url_for, flash
import database
import secret_key
import json
import month

app = Flask(__name__)

app.secret_key = secret_key.secret_key  # Does it have to change periodically?

with open("users_dict.json", 'r') as f:
    users = json.load(f)

base = month.Base()
base.load_from_db("CCG")

data = base.data


@app.route("/")
def hub():
    if not session.get("crm"):
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template("table.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        crm = request.form.get("crm")
        password = request.form.get("password")

        if users.get(crm) == password:
            session["crm"] = crm
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phoneNum")
        email = request.form.get("email")
        crm = request.form.get("crm")
        rqe = request.form.get("rqe")
        password = request.form.get("password")

        database.add_user(crm, name, phone, email, rqe)
        users[crm] = password

        with open("users_dict.json", 'w') as g:
            json.dump(users, g)

        return redirect(url_for("hub"))

    return render_template("signup.html")


@app.route("/protected")
def protected():
    if not session.get("crm"):
        abort(401)
    return render_template("table.html", data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])


@app.route("/table")
def table():
    return render_template("table.html")
