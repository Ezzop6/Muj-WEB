from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired



class NewRecept(FlaskForm):
    nazev_receptu = StringField('nazev_receptu', validators=[DataRequired()])
    submit = SubmitField('submit')
