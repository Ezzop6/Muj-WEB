from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG")
if debug == "True": debug = True
else: debug = False

if debug:
    from forms.forms import LoginForm, RegisterForm
    from my_packages._tools import *
    from database import DbUsersMain
else:
    from api.forms.forms import LoginForm, RegisterForm
    from api.my_packages._tools import *
    from api.database import DbUsersMain


from flask import Blueprint, render_template, request
from flask_login import login_required, logout_user, current_user, login_user, LoginManager, UserMixin

db = DbUsersMain()

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

@main_pages.route('/Login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    if request.method == 'POST':
        if form_login.validate_on_submit():
            if db.login_user(form_login.login.data, form_login.password.data):
                user_id = db.get_user_id(form_login.login.data)
                current_user = User(user_id)
                login_user(current_user)
                return render_template('index.html')
    return render_template('Login.html', form_login=form_login)

@main_pages.route('/Register', methods=['GET', 'POST'])
def register():
    form_register = RegisterForm()
    if request.method == 'POST' and 'Register' in request.form:
        if form_register.validate_on_submit():
            if db.create_user(form_register.login.data, form_register.password.data):
                user_id = db.get_user_id(form_register.login.data)
                current_user = User(user_id)
                login_user(current_user)
                return render_template('index.html')
    return render_template('Register.html', form_register=form_register)

@main_pages.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')