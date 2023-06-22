from flask import Blueprint, render_template

app_blueprint = Blueprint('app_blueprint',__name__)

@app_blueprint.route('/')
def index():
    return render_template("index.html")