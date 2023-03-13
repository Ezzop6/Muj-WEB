from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient ,ASCENDING, DESCENDING
from bson.objectid import ObjectId
from abc import ABC, abstractmethod
# from customtools.fake_users.user_creator import RandomUser
# from customtools.tools import *
import re


class DbConnection(ABC):
    def __init__(self):
        '''Connects to database'''
        load_dotenv(find_dotenv())
        password = os.environ.get("MONGODB_PWD")
        my_conection = f"mongodb+srv://ezzop6:{password}@cluster0.qr7l0pg.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(my_conection)
        
    @abstractmethod
    def create_user(self, user_login, user_password):
        pass
    
    @abstractmethod
    def check_if_user_exists(self, user_login):
        pass
    
    @abstractmethod
    def get_user_id(self, user_login):
        pass
    
    @abstractmethod
    def get_user_login(self, user_id):
        pass
    
    @abstractmethod
    def get_user_role(self, user_id):
        pass
    
    @abstractmethod
    def login_user(self, user_login, user_password):
        pass
    
    
    
        
class DbUsersMain(DbConnection):
    def __init__(self):
        super().__init__()
        self.db = self.client.main.users
        
    def create_user(self, user_login, user_password):
        '''Creates user in database if user does not exist'''
        if self.check_if_user_exists(user_login):
            self.db.insert_one({"login":user_login, "password":user_password, "role":"user"})
        
    def get_user_id(self, user_login):
        '''Returns user id from database'''
        return self.db.find_one({"login":user_login})["_id"]
    
    def get_user_login(self, user_id):
        '''Returns user login from database'''
        return self.db.find_one({"_id":ObjectId(user_id)})["login"]
    
    def get_user_role(self, user_id):
        '''Returns user role from database'''
        return self.db.find_one({"_id":ObjectId(user_id)})["role"]
    
    def check_if_user_exists(self, user_login):
        '''Checks if user exists in database'''
        if self.db.count_documents({"login":user_login}) == 0:
            return True

    def login_user(self, user_login, user_password):
        '''Checks if user exists in database and returns user id'''
        if self.db.count_documents({"login":user_login, "password":user_password}) == 1:
            return self.get_user_id(user_login)
        else:
            return False

class RegisterApp(DbUsersMain):
    def __init__(self):
        super().__init__()
        self.db = self.client.main.register_app
        
    def get_user_id(self, user_login):
        '''Returns user id from database'''
        return self.db.find_one({"login":user_login})["_id"]
    
    def check_if_user_exists(self, user_login):
        return print(super().check_if_user_exists(user_login))
    
    def register_new_app(self, user_login, app_name):
        '''Creates new app in database'''
        if self.check_if_user_exists(user_login):
            user_id = self.get_user_id(user_login)
            self.db.insert_one({"user_id":user_id, "app_name":app_name})
        else:
            print("User does not exist")
        

test = RegisterApp()

test.register_new_app("test", "new_app")