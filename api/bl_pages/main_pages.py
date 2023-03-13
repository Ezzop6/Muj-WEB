from flask import Blueprint, render_template


main_pages = Blueprint('main_pages', __name__)

@main_pages.route('/')
def main_page():
    return render_template('index.html')

@main_pages.route('/about')
def about():
    return render_template('about.html')

@main_pages.route('/base')
def base():
    return render_template('base.html')

@main_pages.route('/projekty')
def projekty():
    return render_template('projekty.html')
