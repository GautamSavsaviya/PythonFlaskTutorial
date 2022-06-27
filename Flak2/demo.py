from flask import *

app = Flask(__name__)


@app.route("/")
def home():
    return "This is home page"


@app.route("/admin")
def admin():
    return "admin page"


@app.route("/student")
def student():
    return "Student page"


@app.route("/management")
def management():
    return "Management page"


@app.route("/user/<name>")
def user(name):
    if name == 'admin':
        return redirect(url_for("admin"))
    elif name == 'student':
        return redirect(url_for("student"))
    elif name == 'management':
        return redirect(url_for("management"))


app.run(debug=True)
