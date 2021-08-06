from flask import render_template

from mobility_app import mobility_app

@mobility_app.route('/')
def index():
    return render_template("index.html")