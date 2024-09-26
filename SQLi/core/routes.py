import os

from flask import *
from jinja2 import exceptions

from .data import *
from .auth import *

app = Flask(
    __name__, 
    static_folder="../static", 
    template_folder="../templates"
)

@app.route('/')
@app.route("/index")
def index():
    return redirect("login")

@app.route("/login", methods=["GET", "POST"])
def login():
    _safety = request.args.get("safety")
    if request.method == "POST":
        staffid = request.form["staffid"]
        password = request.form["password"]
        response, results = check_login(staffid, password, _safety)
        if response:
            return render_template("login.html", response="success", message=results)
        else:
            return render_template("login.html", response="failure")
    return render_template("login.html")

