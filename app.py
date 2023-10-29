from flask import Flask, session, render_template, request, redirect, url_for, jsonify
import secret_key
import functools
import database


app = Flask(__name__)
app.secret_key = secret_key.secret_key  # Does it have to change periodically?

month = database.load_month("CCG", 2023, 10, 0)


def authorization_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("status") is None:
            return redirect(url_for("login"))
        if not session.get("status") == "USER" and not session.get("status") == "ADMIN":
            return redirect(url_for("forbidden"))
        return route(*args, **kwargs)
    return route_wrapper


def admin_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if not session.get("status") == "ADMIN":
            return redirect(url_for("hub"))
        return route(*args, **kwargs)
    return route_wrapper


@app.route("/")
def hub():
    user_status = session.get("status")
    if user_status is None:
        return redirect(url_for("login"))
    if user_status == "PENDING":
        return redirect(url_for("forbidden"))
    if user_status == "USER":
        return redirect(url_for("dashboard"))
    if user_status == "ADMIN":
        return redirect(url_for("dashboard_admin"))
    return redirect(url_for("forbidden"))


@app.route("/dashboard")
@authorization_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard-admin")
@admin_required
def dashboard_admin():
    return render_template("dashboard-admin.html")


@app.route("/calendar/")
@authorization_required
def calendar():
    return render_template("calendar.html", month=month)


@app.route('/calendar_day/<int:day>', methods=['GET'])
def calendar_day(day):
    day_data = month.calendar_dict(day)

    return jsonify({"data": day_data})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        crm = request.form.get("crm")
        password = request.form.get("password")

        if database.get_user_password(crm) and database.get_user_password(crm) == password:
            session["status"] = database.get_user_status(crm)
            # settings.user = crm
            return redirect(url_for("hub"))

    return render_template("login.html")


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    # settings.user = "ADMIN"
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

        database.add_user(crm, password, name, phone, email, rqe)
        session["status"] = database.get_user_status(crm)

        return redirect(url_for("hub"))

    return render_template("signup.html")


@app.route("/forbidden")
def forbidden():
    if session.get("status") is None:
        return redirect(url_for("hub"))
    return render_template("forbidden.html")


@app.route("/protected")
@authorization_required
def protected():
    return render_template("protected.html")


@app.route("/table")
@admin_required
def table():
    return render_template("table.html", data=month.data)
