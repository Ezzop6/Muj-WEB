from flask import Blueprint, render_template


main_pages = Blueprint('modul', __name__)

@main_pages.route('/')
def home():
    return "index page"

@main_pages.route('/about/')
def about():
    return 'About'

@main_pages.route('/hello/')
def hello():
    return 'hello'

@main_pages.route('/base')
def base():
    return render_template('base.html')
