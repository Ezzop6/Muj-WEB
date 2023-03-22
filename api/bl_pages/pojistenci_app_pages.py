from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

if debug:
    from forms.forms_pojistenci_app import *
    from forms.forms import *
    from my_packages._tools import *
    from database import  DbPojistenciProducts, DbUsersPojistenciProducts
else:
    from api.forms.forms_pojistenci_app import *
    from api.forms.forms import *
    from api.my_packages._tools import *
    from api.database import  DbPojistenciProducts, DbUsersPojistenciProducts

from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required, login_user, logout_user





pojistenci_app = Blueprint('pojistenci_app', __name__)

db_user = DbUsersMain()
db_product = DbPojistenciProducts()
db_up = DbUsersPojistenciProducts()



@pojistenci_app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main_pages.main_page'))

@pojistenci_app.route('/')
def index_page():
    '''Main page'''
    return render_template('pojistenci_app/index.html', products = db_product.get_all_products())

@pojistenci_app.route('/login', methods=['GET', 'POST'])
def login_page():
    '''Login page'''
    form_login = LoginForm()
    if form_login.validate_on_submit():
        if db.login_user(form_login.login.data, form_login.password.data):
            user_id = db.get_user_id(form_login.login.data)
            current_user = User(user_id)
            login_user(current_user)
            # Ulož CSRF token do relace
            return render_template('pojistenci_app/index.html')
    return render_template('pojistenci_app/login.html', form_login = form_login)

@pojistenci_app.route('/register', methods=['GET', 'POST'])
def register_page():
    '''Register page'''
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        if db.create_user(form_register.login.data, form_register.password.data):
            user_id = db.get_user_id(form_register.login.data)
            current_user = User(user_id)
            login_user(current_user)
            return redirect(url_for('pojistenci_app.complete_registration', login = form_register.login.data))
    return render_template('pojistenci_app/register.html',
                        form_register = form_register)

@pojistenci_app.route('/register/<login>', methods=['GET', 'POST'])
@login_required
@role_required("user")
def complete_registration(login):
    '''Complete registration page'''
    form_complete_register = CompleteRegisterForm()
    if form_complete_register.validate_on_submit():
        user_id = db_user.get_user_id(login)
        db_user.set_user_name(user_id, form_complete_register.name.data)
        db_user.set_user_surname(user_id, form_complete_register.surname.data)
        db_user.set_user_birthdate(user_id, form_complete_register.birt_date.data)
        return redirect(url_for('pojistenci_app.index_page'))
    return render_template('pojistenci_app/complete_registration.html', 
                        login = login, 
                        form_complete_register = form_complete_register)

@pojistenci_app.route('/user/<login>', methods=['GET', 'POST'])
@login_required
@role_required("user")
def user_page(login):
    '''User page with user data and products'''
    user_form = EditUserDataForm()
    change_password_form = ChangePasswordForm()
    role_form = EditUserRoleForm()
    
    if request.method == 'POST' and 'user_form' in request.form:
        if user_form.validate_on_submit():
            for form, data in user_form.data.items():
                if form == "csrf_token" or form == "submit":
                    continue
                if data != "":
                    db_user.update_user_data(current_user.id, form, data)
            return redirect(url_for('pojistenci_app.user_page', login=login))

    if request.method == 'POST' and 'change_password_form' in request.form:
        if change_password_form.validate_on_submit():
            db_user.change_password(current_user.id, change_password_form.password.data)
            return redirect(url_for('pojistenci_app.user_page', login=login))

    return render_template('pojistenci_app/user.html', 
                        user_form = user_form,
                        role_form = role_form,
                        user = db_user.get_user_data(current_user.id),
                        change_password_form = change_password_form)

# TODO opraveno az sem
@pojistenci_app.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def admin_page():
    '''Admin page with fake user generator'''
    fake_user_generator = AddFakeUserForm()
    
    if fake_user_generator.validate_on_submit():
        db_user.create_fake_users(fake_user_generator.number_users.data)
        
    return render_template('pojistenci_app/admin.html', fake_user_generator = fake_user_generator)

@pojistenci_app.route('/admin/edit_product', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_products_page():
    '''Admin page with products and form for adding new products
    edited products are saved to database'''
    new_produkt = EditProductsForm()
    products = db_product.get_all_products()
    
    if new_produkt.validate_on_submit():
        new_produkt = {"imgs_path":new_produkt.imgs_path.data,"name": new_produkt.name.data, "price": new_produkt.price_per_month.data, "description": new_produkt.description.data}
        db_product.add_product(new_produkt)
        
        return redirect(url_for('pojistenci_app.edit_products_page'))
    return render_template('pojistenci_app/all_products.html', new_produkt = new_produkt, products = products)

@pojistenci_app.route('/admin/edit_user', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_users_page():
    sorting_form = FindUserForm()
    
    sort_direction = request.args.get('sort_direction', 'asc')
    sort_by = request.args.get('sort_by', 'login')
    
    users = db_user.sort_users_by(sort_direction, sort_by)
    if sorting_form.validate_on_submit():
        users = db_user.find_users_by(sorting_form.search_by.data, sorting_form.search.data)
        
    return render_template('pojistenci_app/all_users.html', 
                        users = users,
                        sorting_form = sorting_form,
                        sort_direction = sort_direction)

@pojistenci_app.route('/admin/edit_user/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_user(id):
    '''Admin page with form for editing users'''
    user_form = EditUserDataForm()
    change_password_form = ChangePasswordForm()
    role_form = EditUserRoleForm()
    user_id = id
    
    if request.method == 'POST' and 'user_form' in request.form:
        if user_form.validate_on_submit():
            for form, data in user_form.data.items():
                if form == "csrf_token" or form == "submit":
                    continue
                if data != "":
                    db_user.update_user_data(user_id, form, data)
                    
    if request.method == 'POST' and 'change_password_form' in request.form:
        if change_password_form.validate_on_submit():
            db_user.update_user_data(current_user.id, "password", change_password_form.password.data)

    if request.method == 'POST' and 'change_role_form' in request.form:
        if role_form.validate_on_submit():
            db_user.update_user_data(user_id, "role", role_form.role.data)
            cprint("Welcome new admin!")
            
    return render_template('pojistenci_app/user.html', user_form = user_form,
                        change_password_form = change_password_form,
                        role_form = role_form, 
                        user = db_user.get_user_data(user_id))

@pojistenci_app.route('/admin/edit_user/delete/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def delete_user(id):
    '''Admin page with form for editing users'''
    form = YesNoForm()
    user = db_user.get_user_data(id)
    if form.validate_on_submit():
        if form.yes.data:
            db_user.delete_user(id)
            return redirect(url_for('pojistenci_app.edit_users_page'))
        else: return redirect(url_for('pojistenci_app.edit_users_page'))
    return render_template('pojistenci_app/delete_product.html', product = user , form = form)

@pojistenci_app.route('/base', methods=['GET', 'POST'])
def base_page():
    '''base page for testing purposes'''
    return render_template('base.html')

#TODO predelat na neco lepe citelneho neco jako je admin edit user
# je treba predelat i cely formular pravdepodobne cast databaze
@pojistenci_app.route('/admin/edit_product/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def edit_product(id):
    '''Admin page with form for editing products'''
    edited_product = EditProduct()
    product = db_product.get_product_by_name(id)
    edited_product.description.render_kw = {"placeholder": product["description"]}
    edited_product.price_per_month.render_kw = {"placeholder": product["price"]}
    if edited_product.validate_on_submit():
        db_product.add_product_imgs_path(id, edited_product.imgs_path.data)
        db_product.update_product(id, edited_product.description.data, edited_product.price_per_month.data)
        return redirect(url_for('pojistenci_app.edit_products_page')) 
    return render_template('pojistenci_app/edit_product.html', product = product, form = edited_product)

@pojistenci_app.route('/admin/delete/<id>', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def delete_product(id):
    '''delete product page with confirmation'''
    form = YesNoForm()
    product = db_product.get_product_by_name(id)
    if form.validate_on_submit():
        if form.yes.data == True:
            db_product.delete_product(id)
            return redirect(url_for('pojistenci_app.edit_products_page'))
        else: return redirect(url_for('pojistenci_app.edit_products_page'))
    return render_template('pojistenci_app/delete_product.html', product = product , form = form)

