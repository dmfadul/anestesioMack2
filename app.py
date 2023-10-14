from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        print(name, password)
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")
