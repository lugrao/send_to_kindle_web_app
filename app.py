from flask import Flask, render_template, request
from flask_login import LoginManager
from html2epub2kindle import html2epub2kindle
import os

login_manager = LoginManager()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/url", methods=['POST'])
def html2kindle():
    url = request.form.get("url")
    password = request.form.get("password")

    if not url:
        return render_template("message.html", message="You must provide a URL.")

    
    if password != os.environ.get("APP_PASSWORD"):
        return render_template("message.html", message="Incorrect password.")

    html2epub2kindle(url)
    
    return render_template(
        "message.html",
        message="The article was sent to your kindle. Apparently."
        )
