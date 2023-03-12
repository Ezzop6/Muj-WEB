from flask import Blueprint, render_template

modul = Blueprint('modul', __name__)

@modul.route('/')
def home():
    return "index page"

@modul.route('/about/')
def about():
    return 'About'


@modul.route('/hello/')
def hello():
    return 'hello'
