from flask import Blueprint, render_template

bl_main_pages = Blueprint('modul', __name__)

@bl_main_pages.route('/')
def home():
    return "index page"

@bl_main_pages.route('/about/')
def about():
    return 'About'


@bl_main_pages.route('/hello/')
def hello():
    return 'hello'
