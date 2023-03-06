from flask import Flask, render_template
from html2epub2kindle import html2epub2kindle

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:url>")
def html2kindle(url):
    html2epub2kindle(url)
    return "The article was sent to your kindle. Apparently."
