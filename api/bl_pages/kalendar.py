from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

if debug:
    from forms.smenost_app.forms import Kalendar
else:
    from api.forms.smenost_app.forms import Kalendar

from flask import Blueprint, render_template, request, redirect, url_for

import calendar
from datetime import date

kalendar = Blueprint('kalendar', __name__)

@kalendar.route('/about_app', methods=['GET', 'POST'])
def about_app():
    return render_template('kalendar/about_app.html')

@kalendar.route('/', methods=['GET', 'POST'])
def main_page():
    form = Kalendar()

    # Nastavi defaultni hodnoty pro rok a mesic
    year = int(form.year.default)
    month = int(form.month.default)
    today = (date.today().year,date.today().month,date.today().day)

    if form.validate():
        
        year = int(form.year.data)
        month = int(form.month.data)
        
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(year, month)
        return render_template('kalendar/index.html',
                        month_days=month_days, 
                        current_calendar=(year, month), 
                        form=form,
                        today=today
                        )
        
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('kalendar/index.html',
                        month_days=month_days, 
                        current_calendar=(year, month), 
                        form=form,
                        today=today
                        )
    
    
@kalendar.route('/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def day_page(year, month, day):
    day_to_edit = date(year, month, day)
    return render_template('kalendar/day.html', year=year, month=month, day=day, day_to_edit=day_to_edit)