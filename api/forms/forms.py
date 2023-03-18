from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG")
if debug == "True": debug = True
else: debug = False

if debug:
    from database import DbUsersMain
else:
    from api.database import DbUsersMain
    
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError

import datetime

db = DbUsersMain()


forbidden_words = ["admin","root","administrator"] # forbidden words in name, surname and login
forrbiden_letters = "!@#$%^&*()_+{}|:<>?/.,;'[]\=-`~"

class CustomTest:
    @staticmethod
    def validate_password(password, password2):
        password = password.data
        special_characters = "!@#$%^&*()_+|:<>?[]\;',./`~ěščřžýáíéúůťďňóĚŠČŘŽÝÁÍÉÚŮŤĎŇÓ"
        min_length = 8
        digit = sum(1 for letter in password if letter.isdigit())
        special = sum(1 for letter in password if letter in special_characters)
        small_letter = sum(1 for letter in password if letter.islower())
        big_letter = sum(1 for letter in password if letter.isupper())
        
        if min_length > len(password):
            raise ValidationError(f"Heslo musí mít minimálně {min_length} znaků")
        elif digit == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jedno číslo")
        elif special == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jeden speciální znak")
        elif small_letter == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jedno malé písmeno")
        elif big_letter == 0:
            raise ValidationError("Heslo musí obsahovat alespoň jedno velké písmeno")
        elif password != password2:
            raise ValidationError("Hesla se neshodují")
        

    
class LoginForm(FlaskForm):
    login = StringField('Login', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('Heslo', [validators.Length(min=8, max=25), validators.DataRequired()])
    submit = SubmitField('Přihlásit se')
    
    def validate_login(self, login):
        login = login.data
        if not db.check_if_user_exists(login) == None:
            raise ValidationError(f"Login: {login} neexistuje")
        
    def validate_password(self, password):
        login = self.login.data
        password = password.data
        if not db.login_user(login, password):
            raise ValidationError("Špatné jméno nebo heslo")
    
class RegisterForm(FlaskForm):
    login = StringField('Login', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('Heslo', [validators.Length(min=8, max=25), validators.DataRequired()])
    password2 = PasswordField('Heslo znovu', [validators.Length(min=8, max=25), validators.DataRequired()])
    submit = SubmitField('Registrovat se')
    
    
    def validate_login(self, login):
        login = login.data
        if login in forbidden_words:
            raise ValidationError(f"nesmíš použít tento login: {login}")
        if db.check_if_user_exists(login) == None:
            raise ValidationError(f"Uživatel s loginem {login} již existuje")
    
    def validate_password(self, password):
        CustomTest.validate_password(password, self.password2.data)