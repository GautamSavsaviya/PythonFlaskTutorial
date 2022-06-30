# Importing required modules.
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

# Open and read config.json file to read different parameters dynamically.
with open('config.json', 'r') as config:
    params = json.load(config)["params"]

# Create variable named local_host for determine server is local or production server.
local_host = True

# Create instance of Flask class named app.
app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USER=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_password']
)
mail = Mail(app)
# Check website is using local server or not, if it is use local server than connect the app with local uri otherwise use production server.
if local_host:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(14), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)


@app.route("/")
def hello_world():
    return render_template("index.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html", params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, email=email, phone_no=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            f"New message from {name}",
            sender=email,
            recipients=[params['gmail_user']],
            body=f"{message} \n {phone}"
        )

    return render_template("contact.html", params=params)


@app.route("/post")
def post():
    return render_template("post.html", params=params)


app.run(debug=True)
