from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

if debug:
    from database import DbUsersMain
else:
    from api.database import DbUsersMain
    
from flask_wtf import FlaskForm
from wtforms import  SelectField, SubmitField

import datetime

db = DbUsersMain()

class Kalendar(FlaskForm):
    year = SelectField('Rok', choices=[(year, year) for year in range(2019, datetime.date.today().year + 5)],
        default = datetime.date.today().year)
    month = SelectField('Měsíc', choices=[(month, month) for month in range(1, 13)],
        default = datetime.date.today().month)
    submit = SubmitField('Zobrazit')