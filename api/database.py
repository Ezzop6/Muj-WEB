from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

if debug:
    from my_packages._tools import *
else:
    from api.my_packages._tools import *
    
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient ,ASCENDING, DESCENDING
from bson.objectid import ObjectId
from cryptography.fernet import Fernet
import datetime

import re


class DbConnection:
    def __init__(self):
        '''Connects to database'''
        load_dotenv(find_dotenv())
        password = os.environ.get("MONGODB_PWD")
        my_conection = f"mongodb+srv://ezzop6:{password}@cluster0.qr7l0pg.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(my_conection)

    
        
class DbUsersMain(DbConnection):
    def __init__(self):
        super().__init__()
        if debug:
            self.user_db = self.client.test.users
            self.user_key = self.client.test.keys
        else:
            self.user_db = self.client.main.users
            self.user_key = self.client.main.keys
        
        
    def create_user(self, user_login, user_password):
        '''Creates user in database if user does not exist'''
        if self.check_if_user_exists(user_login):
            key = self.generate_key()
            password = self.encript_data(user_password,key)
            register_time = self.current_time()
            
            self.user_db.insert_one({"login":user_login, "password":password, "role":"user",
                                    "register_time":register_time, "last_login":register_time})
            
            user_id = self.get_user_id(user_login)
            self.user_key.insert_one({"_id":user_id, "key":key})
            return True
        else:
            return False
            
    def login_user(self, user_login, user_password):
        '''Checks if user exists and if password is correct'''
        if not self.check_if_user_exists(user_login):
            user_id = self.get_user_id(user_login)
            user_key = self.get_user_key(user_id)
            encripted_password = self.get_user_password(user_id)
            decripted_password = self.decript_data(encripted_password, user_key)
            if user_password == decripted_password:
                self.update_user_last_login(user_id)  
                return True
            else:
                return False
        else:
            return False
    
    def change_password(self, user_id, new_password):
        '''Changes user password'''
        user_key = self.get_user_key(user_id)
        print("user key =",user_key)
        print("new password =",new_password)
        
        encripted_password = self.encript_data(new_password, user_key)
        print("encripted password =",encripted_password)
        self.user_db.update_one({"_id": ObjectId(user_id)}, {"$set":{"password":encripted_password}})
        print("Password changed")
    
    def check_if_user_exists(self, user_login):
        '''Checks if user exists in database'''
        if self.user_db.count_documents({"login":user_login}) == 0:
            return True
    
    def current_time(self):
        '''Returns current time'''
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%d.%m.%Y %H:%M:%S")
        return current_time

    # key functions for encription and decription
    def generate_key(self):
        '''Creates key for user'''
        key = Fernet.generate_key()
        return key
        
    def encript_data(self, data_to_encript, key):
        '''Creates key for user'''
        fernet = Fernet(key)
        encripted_data = fernet.encrypt(data_to_encript.encode())
        return encripted_data
    
    def decript_data(self, data_to_decript, key):
        fernet = Fernet(key)
        decripted_data = fernet.decrypt(data_to_decript).decode()
        return decripted_data
    
    # functions for getting data from database
    def get_user_id(self, user_login):
        '''Returns user id from database'''
        return self.user_db.find_one({"login":user_login})["_id"]
    
    def get_user_data(self, user_id):
        '''Returns user'''
        user = self.user_db.find_one({"_id": ObjectId(user_id)})
        return user
    
    def get_user_key(self, user_id):
        '''Returns user key from database'''
        return self.user_key.find_one({"_id":ObjectId(user_id)})["key"]
    
    def get_user_login(self, user_id):
        '''Returns user login from database'''
        return self.user_db.find_one({"_id":ObjectId(user_id)})["login"]
    
    def get_user_password(self, user_id):
        '''Returns user password from database'''
        return self.user_db.find_one({"_id":ObjectId(user_id)})["password"]
    
    def get_user_role(self, user_id):
        '''Returns user role from database'''
        return self.user_db.find_one({"_id":ObjectId(user_id)})["role"]
    
    # functions for updating data in database
    def update_user_last_login(self, user_id):
        '''Updates user last login time'''
        last_login = self.current_time()
        self.user_db.update_one({"_id":ObjectId(user_id)}, {"$set":{"last_login":last_login}})
        
    def update_user_data(self, user_id, update, update_value):
        '''Updates user data'''
        self.user_db.update_one({"_id": ObjectId(user_id)}, {"$set": {update: update_value}})
        # cprint(f"User {user_id} updated with {update} = {update_value}")
        
    # function for adding data to database
    def set_user_name(self, user_id, name):
        '''Sets user name'''
        self.user_db.update_one({"_id":ObjectId(user_id)}, {"$set":{"name":name}})
    
    def set_user_surname(self, user_id, surname):
        '''Sets user surname'''
        self.user_db.update_one({"_id":ObjectId(user_id)}, {"$set":{"surname":surname}})
        
    def set_user_birthdate(self, user_id, birthdate):
        '''Sets user birthdate'''
        self.user_db.update_one({"_id":ObjectId(user_id)}, {"$set":{"birthdate":birthdate.strftime('%Y.%m.%d')}})
    
class DbKalendar(DbUsersMain):
    def __init__(self):
        super().__init__()
        if debug:
            self.shift = self.client.test.shift_calendar
        else:
            self.shift = self.client.main.shift_calendar
        
    def create_user_kalendar(self, user_id):
        '''Creates user kalendar in database'''
        self.shift.insert_one({"_id":ObjectId(user_id)})
        
class DbReceptar(DbUsersMain):
    def __init__(self):
        super().__init__()
        if debug:
            self.receptar = self.client.test.receptar
        else:
            self.receptar = self.client.main.receptar
        
    def create_new_recept(self, user_id, name):
        '''Creates new recept in database'''
        self.receptar.insert_one({"_id":ObjectId(user_id), "name":name})
        

class DbPojistenciProducts(DbUsersMain):
    def __init__(self):
        super().__init__()
        self.db = self.client.pojistenci_uzivatele.products
        
    def add_product(self, product):
        '''Adds product to database'''
        self.db.insert_one(product)
        
    def get_all_products(self):
        '''Returns all products'''
        return self.db.find()
    
    def check_if_name_exists(self, product_name):
        '''Checks if product exists'''
        if self.db.count_documents({"name": product_name}) > 0:
            cprint("Product already exists")
            return True
    
    def get_product_by_name(self,produkt_name):
        '''Returns product by name'''
        produkt = self.db.find_one({"name": produkt_name})
        return produkt
    
    def delete_product(self, produkt_name):
        '''Deletes product by name'''
        self.db.delete_one({"name": produkt_name})
        
    def get_product_id(self,product_name):
        '''Returns product id'''
        return self.db.find_one({"name": product_name})["_id"]
    
    def add_product_imgs_path(self,product_name,imgs_path):
        self.db.update_one({"name": product_name}, {"$set": {"imgs_path": imgs_path}})
    
    def update_product(self,product_name,description,price_per_month):
        '''Updates product description and price by name'''
        self.db.update_one({"name": product_name}, {"$set": {"description": description, "price": price_per_month}})
        
class DbUsersPojistenciProducts(DbUsersMain):
    def __init__(self):
        super().__init__()
        if debug:
            self.db = self.client.test.users_product
        else:
            self.db = self.client.pojistenci_uzivatele.users_product