from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

if debug:
    from database_pojistenci import DbProducts
else:
    from api.database_pojistenci import DbProducts

from flask_wtf import FlaskForm
from wtforms import  TextAreaField, IntegerField, SelectField ,widgets, StringField, PasswordField, SubmitField, DateField, validators,ValidationError
import datetime


db_product = DbProducts()

forbidden_words = ["admin","root","administrator"] # forbidden words in name, surname and login
forrbiden_letters = "!@#$%^&*()_+{}|:<>?/.,;'[]\=-`~"

class CustomTest:
    @staticmethod
    def contains_forbidden_letters(data):
        if len(data) == 0:
            return
        for letter in data:
            if letter in forrbiden_letters:
                return True
            
    @staticmethod        
    def contains_digit(data):
        if len(data) == 0:
            return
        for letter in data:
            if letter.isdigit():
                return True
            
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
        
    @staticmethod
    def validate_name(name):
        name = name.data
        if len(name) == 0:
            return
        if len(name) < 2:
            raise ValidationError(f"Jméno musí mít alespoň 2 znaky: {name}")
        if name in forbidden_words:
            raise ValidationError(f"nesmíš použít toto jméno: {name}")
        if CustomTest.contains_forbidden_letters(name):
            raise ValidationError(f"nesmíš použít tyto znaky v jménu: {forrbiden_letters}")
        if CustomTest.contains_digit(name):
            raise ValidationError(f"nesmíš použít číslice v jménu: {name}")
        
    @staticmethod
    def validate_street_number(street_number):
        street_number = street_number.data
        if len(street_number) == 0:
            return
        if len(street_number) > 7:
            raise ValidationError(f"Číslo domu musí mít maximálně 6 znaků: {street_number}")
        for letter in street_number:
            if letter == "/": # asi to fakt zbytecne komplikuju
                continue
            if not letter.isdigit():
                raise ValidationError(f"Číslo domu musí být číslo: {street_number}")
        
            
    @staticmethod
    def validate_zip_code(zip_code):
        zip_code = zip_code.data
        if len (zip_code) == 0:
            return
        if len(zip_code) != 5:
            raise ValidationError(f"PSČ musí mít 5 číslic: {zip_code}")
        for letter in zip_code:
            if not letter.isdigit():
                raise ValidationError(f"PSČ musí být číslo: {zip_code}")
            
    @staticmethod
    def validate_street(street):
        street = street.data
        if len(street) == 0:
            return
        if len(street) < 2:
            raise ValidationError(f"Ulice musí mít alespoň 2 znaky: {street}")
        for letter in street:
            if letter.isdigit():
                raise ValidationError(f"Ulice nesmí obsahovat číslice: {street}")
        for letter in street:
            if letter in forrbiden_letters:
                raise ValidationError(f"Ulice nesmí obsahovat tyto znaky: {forrbiden_letters}")
            
    @staticmethod
    def validate_city(city):
        city = city.data
        if len(city) == 0:
            return
        if len(city) < 2:
            raise ValidationError(f"Město musí mít alespoň 2 znaky: {city}")
        for letter in city:
            if letter.isdigit():
                raise ValidationError(f"Město nesmí obsahovat číslice: {city}")
        for letter in city:
            if letter in forrbiden_letters:
                raise ValidationError(f"Město nesmí obsahovat tyto znaky: {forrbiden_letters}")
        
    
class CompleteRegisterForm(FlaskForm):
    name = StringField("Jméno", widget = widgets.Input(input_type = "text"),
                        validators=[validators.DataRequired(message="Musíte zadat jméno"),
                                    validators.Length(min=2, max=20, message="Jméno musí mít 2 až 20 znaků")])
    surname = StringField("Příjmení", widget = widgets.Input(input_type = "text"),
                        validators=[validators.DataRequired(message="Musíte zadat příjmení"),
                                    validators.Length(min=2, max=20, message="Příjmení musí mít 2 až 20 znaků")])
    birt_date = DateField("Datum narození", widget = widgets.Input(input_type = "date"),
                        validators=[validators.DataRequired(message="Musíte zadat datum narození")])
    submit = SubmitField("Uložit")
    
    def validate_name(self, name):
        CustomTest.validate_name(name)
        
    def validate_surname(self, surname):
        CustomTest.validate_name(surname)
        
    def validate_birt_date(self, birt_date):
        birt_date = birt_date.data
        if birt_date > datetime.date.today():
            raise ValidationError(f"Sorry tahle aplikace nepodporuje cesty časem: {birt_date}")



class EditProductsForm(FlaskForm):
    name = StringField("Název", widget = widgets.Input(input_type = "text"),
        validators = [validators.DataRequired(message="Musíte zadat název produktu"),
                    validators.Length(min=3, max=200, message="Název musí mít 3 až 200 znaků")])
    description = TextAreaField("Popis", widget = widgets.TextArea(),
        validators = [validators.DataRequired(message="Musíte zadat popis produktu"),
                    validators.Length(min=20, max=2000, message="Popis musí mít 20 až 2000 znaků")])
    price_per_month = IntegerField("Cena za měsíc", widget = widgets.Input(input_type = "number"),
        validators = [validators.DataRequired(message="Musíte zadat cenu za měsíc")])
    imgs_path = StringField("Složka k obrázkům", widget = widgets.Input(input_type = "text"))
    submit = SubmitField("Potvrdit")
    
    def validate_price_per_month(self, price_per_month):
        price_per_month = price_per_month.data
        if price_per_month < 0:
            raise ValidationError(f"Cena za měsíc musí být kladná: {price_per_month}")
        
    def validate_name(self, name):
        name = name.data
        if name in forbidden_words:
            raise ValidationError(f"nesmíš použít tento název: {name}")
        if db_product.check_if_name_exists(name) != None:
            raise ValidationError(f"Produkt s názvem {name} již existuje")
        
class EditProduct(FlaskForm):
    description = TextAreaField("Popis", widget = widgets.TextArea(),
        validators = [validators.DataRequired(message="Musíte zadat popis produktu"),
                    validators.Length(min=20, max=2000, message="Popis musí mít 20 až 2000 znaků")])
    price_per_month = IntegerField("Cena za měsíc", widget = widgets.Input(input_type = "number"),
        validators = [validators.DataRequired(message="Musíte zadat cenu za měsíc")])
    imgs_path = StringField("Složka k obrázkům", widget = widgets.Input(input_type = "text"))
    submit = SubmitField("Potvrdit")
    
    def validate_price_per_month(self, price_per_month):
        price_per_month = price_per_month.data
        if price_per_month < 0:
            raise ValidationError(f"Cena za měsíc musí být kladná: {price_per_month}")
    
class YesNoForm(FlaskForm):
    yes = SubmitField("Ano")
    no = SubmitField("Ne")
    
class AddFakeUserForm(FlaskForm):
    number_users = IntegerField("Vytvor uzivatele", widget = widgets.Input(input_type = "number"))
    submit = SubmitField("Potvrdit")
    
    def validate_number_users(self, number_users):
        number_users = number_users.data
        if number_users > 100:
            raise ValidationError(f"Povoleno je max 100 : {number_users}")
        
class EditUserDataForm(FlaskForm):
    name = StringField("Jméno", widget = widgets.Input(input_type = "text"))
    surname = StringField("Příjmení", widget = widgets.Input(input_type = "text"))
    city = StringField("Město", widget = widgets.Input(input_type = "text"))
    street = StringField("Ulice", widget = widgets.Input(input_type = "text"))
    street_number = StringField("Číslo popisné", widget = widgets.Input(input_type = "text"))
    zip_code = StringField("PSČ", widget = widgets.Input(input_type = "text"))
    email = StringField("Email", widget = widgets.Input(input_type = "email"))
    submit = SubmitField("Uložit")
    
    def validate_name(self, name):
        CustomTest.validate_name(name)
        
    def validate_surname(self, surname):
        CustomTest.validate_name(surname)
        
    def validate_city(self, city):
        CustomTest.validate_city(city)
        
    def validate_street(self, street):
        CustomTest.validate_street(street)
        
    def validate_street_number(self, street_number):
        CustomTest.validate_street_number(street_number)
        
    def validate_zip_code(self, zip_code):
        CustomTest.validate_zip_code(zip_code)
        
    
class ChangePasswordForm(FlaskForm):
    password = PasswordField("Heslo", widget=widgets.Input(input_type = "password"))
    password2 = PasswordField("Zopakujte heslo", widget = widgets.Input(input_type = "password"))
    change_password = SubmitField("Uložit")
    
    if password != "" or password2 != "":
        def validate_password(self, password):
            CustomTest.validate_password(password, self.password2.data)

class EditUserRoleForm(FlaskForm):
    role = SelectField("Role", choices = [("user", "user"), ("admin", "admin")])
    submit = SubmitField("Uložit")
    
class FindUserForm(FlaskForm):
    search_by = SelectField("Hledat podle", choices = [("login", "login"), ("name", "jména"), ("surname", "příjmení"),
        ("city", "města"), ("street", "ulice"), ("street_number", "čísla popisného"), ("zip_code", "PSČ"), ("email", "email"),
        ("birth_date", "datum narození")])
    search = StringField("Hledat", widget = widgets.Input(input_type = "text"))
