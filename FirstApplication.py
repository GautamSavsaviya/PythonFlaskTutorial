from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello World...!123</p>"


@app.route("/home")
def home():
    return "WelCome to home page"


app.run(debug=True)

