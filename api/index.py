# Description: Main file of the app
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG")
if debug == "True": debug = True

if debug:
    user_for_debuging = os.environ.get("USER_FOR_DEBUGING")
    from my_packages._tools import *
    from bl_pages.main_pages import main_pages
    from bl_pages.pojistenci_app_pages import pojistenci_app_pages
    from bl_pages.smenost_app_pages import smenost_app_pages
    from database import DbUsersMain
else:
    from api.my_packages._tools import *
    from api.bl_pages.main_pages import main_pages
    from api.bl_pages.pojistenci_app_pages import pojistenci_app_pages
    from api.bl_pages.smenost_app_pages import smenost_app_pages
    from api.database import DbUsersMain

from flask import Flask, render_template, request, redirect, url_for, g, session, abort
from flask_login import current_user, login_required, LoginManager, UserMixin, login_user, logout_user

import os
from functools import wraps

Db = DbUsersMain()


app = Flask(__name__)
app.secret_key = random_secret_key()
app.config['PERMANENT_SESSION_LIFETIME'] = 60000 # time to logout user

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(main_pages, url_prefix='/')
app.register_blueprint(pojistenci_app_pages, url_prefix='/pojistenci_app')
app.register_blueprint(smenost_app_pages, url_prefix='/KalendarSmen_app')

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = Db.get_user_role(self.id)
        self.login = Db.get_user_login(self.id)
        
@login_manager.user_loader
def load_user(user_id):
    '''Callback to reload the user object from the user ID stored in the session'''
    return User(user_id)


@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]
        


if debug:
    @app.route('/login_test_user')
    def login_test_user():
        '''Login test user'''
        if user_for_debuging == "admin":
            current_user = User("640f7917bf613a7f3479c332")
        else:
            current_user = User("string")#TODO doplnit id testovaciho uzivatele
        login_user(current_user)
        return redirect(url_for('main_pages.main_page'))
    
    @app.route('/logout_test_user')
    def logout_test_user():
        '''Logout test user'''
        logout_user()
        return redirect(url_for('main_pages.main_page'))
    
if __name__ == '__main__':
    if debug:
        app.debug = True
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    app.jinja_env.globals.update(get_random_produkt_img = get_random_produkt_img)
    app.jinja_env.globals.update(debug = debug)
    app.run(host=host, port=port)