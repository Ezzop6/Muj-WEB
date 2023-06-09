from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

if debug:
    from my_packages._tools import *
    from my_packages.vtipky import error_page_joke
    from bl_pages.main_pages import main_pages
    from bl_pages.pojistenci_app_pages import pojistenci_app
    from bl_pages.kalendar import kalendar
    from bl_pages.klobasovnik import klobasovnik
    from database import DbUsersMain
    
else:
    from api.my_packages._tools import *
    from api.my_packages.vtipky import error_page_joke
    from api.bl_pages.main_pages import main_pages
    from api.bl_pages.pojistenci_app_pages import pojistenci_app
    from api.bl_pages.kalendar import kalendar
    from api.bl_pages.klobasovnik import klobasovnik
    from api.database import DbUsersMain
    

from flask_session import Session
from flask import Flask, render_template, redirect, url_for, g, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from redis import Redis
import os

db = DbUsersMain()

login_manager = LoginManager()

# nastaveni redisu
redis_password = os.environ.get("REDIS_PWD")
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
redis_client = Redis( host = redis_host, port = redis_port, password = redis_password )

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
csrf = CSRFProtect(app)

app.config['PERMANENT_SESSION_LIFETIME'] = 7200 # time to logout user
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_client
app.config['SESSION_USE_SIGNER'] = True
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")

Session(app)



app.register_blueprint(main_pages, url_prefix='/')
app.register_blueprint(pojistenci_app, url_prefix='/pojistenci_app')
app.register_blueprint(kalendar, url_prefix='/kalendar')
app.register_blueprint(klobasovnik, url_prefix='/klobasovnik')

login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]
        
@login_manager.user_loader
def load_user(user_id):
    '''Callback to reload the user object from the user ID stored in the session'''
    return User(user_id)

        
'''error pages'''
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def access_denied(error):
    error_code = str(error.code)
    message = error_page_joke(error_code)
    if error_code == '401':
        return render_template('401.html', error = error, message = message)
    elif error_code == '403':
        return render_template('403.html', error = error, message = message)
    elif error_code == '404':
        return render_template('404.html', error = error, message = message)

# for debuging
if debug:
    @app.route('/login_test_user')
    def login_test_user():
        '''Login test user'''
        current_user = User("641aafa9285f4a3f68fa3f3e")
        login_user(current_user)
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