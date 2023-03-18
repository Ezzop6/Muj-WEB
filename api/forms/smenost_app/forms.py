from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

from flask_wtf import FlaskForm
from wtforms import  SelectField, SubmitField

import datetime

months = [(1, 'Leden'), (2, 'Únor'), (3, 'Březen'), (4, 'Duben'), (5, 'Květen'), (6, 'Červen'), (7, 'Červenec'), (8, 'Srpen'), (9, 'Září'), (10, 'Říjen'), (11, 'Listopad'), (12, 'Prosinec')]
class Kalendar(FlaskForm):
    year = SelectField('Rok', choices=[(year, year) for year in range(2023, datetime.date.today().year + 5)],
        default = datetime.date.today().year)
    month = SelectField('Měsíc', choices=[month for month in months],
        default = datetime.date.today().month)
    submit = SubmitField('Zobrazit')