# tomusi byt vsude kde se neco importuje
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG")
if debug == "True": debug = True
else: debug = False

if debug:
    user_for_debuging = os.environ.get("USER_FOR_DEBUGING")
    from my_packages._tools import *
    from my_packages.vtipky import error_page_joke
    from bl_pages.main_pages import main_pages
    from bl_pages.pojistenci_app_pages import pojistenci_app_pages
    from bl_pages.smenost_app_pages import smenost_app_pages
    from database import DbUsersMain
else:
    from api.my_packages._tools import *
    from api.my_packages.vtipky import error_page_joke
    from api.bl_pages.main_pages import main_pages
    from api.bl_pages.pojistenci_app_pages import pojistenci_app_pages
    from api.bl_pages.smenost_app_pages import smenost_app_pages
    from api.database import DbUsersMain


from flask import Flask, render_template, request, redirect, url_for, g, session, abort
from flask_login import current_user, login_required, LoginManager, UserMixin, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
import os

db = DbUsersMain()


app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = random_secret_key()
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # time to logout user
app.config['WTF_CSRF_TIME_LIMIT'] = 3600

login_manager.init_app(app)


app.register_blueprint(main_pages, url_prefix='/')
app.register_blueprint(pojistenci_app_pages, url_prefix='/pojistenci_app')
app.register_blueprint(smenost_app_pages, url_prefix='/KalendarSmen_app')

@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]
        
        
'''error pages'''
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def access_denied(error):
    error_code = str(error.code)
    message = error_page_joke(error_code)
    if error_code == '401':
        return render_template('401.html', error=error, message=message)
    elif error_code == '403':
        return render_template('403.html', error=error, message=message)
    elif error_code == '404':
        return render_template('404.html', error=error, message=message)
    
# for debuging
if debug:
    @app.route('/login_test_user')
    def login_test_user():
        '''Login test user'''
        current_user = User("6411e442735e17571d1edc4a")
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
        cprint("Debug mode is ON")
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    app.jinja_env.globals.update(get_random_produkt_img = get_random_produkt_img)
    app.jinja_env.globals.update(debug = debug)
    app.run(host=host, port=port)