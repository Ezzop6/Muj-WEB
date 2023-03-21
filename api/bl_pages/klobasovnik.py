from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

if debug:
    from forms.forms_klobasovnik import NewRecept
    from my_packages._tools import *
    from database import DbReceptar
else:
    from api.forms.forms_klobasovnik import NewRecept
    from api.my_packages._tools import *
    from api.database import DbReceptar

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
db = DbReceptar()

klobasovnik = Blueprint('klobasovnik', __name__)

@role_required('admin')
@login_required
@klobasovnik.route('/', methods=['GET', 'POST'])
def main_page():
    print(current_user)
    form = NewRecept()
    if form.validate_on_submit():
        
        return redirect(url_for('klobasovnik.new_recept'))
    return render_template('klobasovnik/index.html',
                            form=form,
                            )
    
@role_required('admin')
@login_required
@klobasovnik.route('/new_recept', methods=['GET', 'POST'])
def new_recept():


    return render_template('klobasovnik/new_recept.html',
                            )
    
@role_required('admin')
@login_required
@klobasovnik.route('/about_app', methods=['GET', 'POST'])
def about_app():
    return render_template('klobasovnik/about_app.html')
