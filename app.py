from flask import Flask, session, render_template, request, abort, redirect, url_for, flash, jsonify
import session_var
import secret_key
import database
import json

app = Flask(__name__)

app.secret_key = secret_key.secret_key  # Does it have to change periodically?

with open("users_dict.json", 'r') as f:
    users = json.load(f)

month = database.load_month("CCG", 2023, 11)


@app.route("/")
def hub():
    if not session.get("crm"):
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return redirect(url_for("calendar"))


@app.route("/calendar/")
def calendar():
    return render_template("calendar.html", month=month)


@app.route('/calendar_day/<int:day>', methods=['GET'])
def calendar_day(day):
    return jsonify({"data": month.data_dict_days.get(month.dict_day_key(day), "data not found")})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        crm = request.form.get("crm")
        password = request.form.get("password")

        if users.get(crm) == password:
            session["crm"] = crm
            session_var.user = crm
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    session_var.user = "ADMIN"
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

        database.save_user(crm, name, phone, email, rqe)
        users[crm] = password

        with open("users_dict.json", 'w') as g:
            json.dump(users, g)

        return redirect(url_for("hub"))

    return render_template("signup.html")


@app.route("/protected")
def protected():
    if not session.get("crm"):
        abort(401)
    return render_template("protected.html")


@app.route("/table")
def table():
    return render_template("table.html", data=month.table)
