from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG")
if debug == "True": debug = True
else: debug = False

from flask import Blueprint, render_template

if debug:
    from forms.forms import LoginForm, RegisterForm
else:
    from api.forms.forms import LoginForm, RegisterForm

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

@main_pages.route('/LoginRegister')
def login_register():
    form_register = RegisterForm()
    form_login = LoginForm()
    return render_template('LoginRegister.html',
                           form_register=form_register,
                           form_login=form_login)
