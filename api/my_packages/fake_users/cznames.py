from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
debug = os.environ.get("DEBUG") == "True"

from random import choice

if debug:
    names = {
        False:"./api/my_packages/fake_users/jmena/male.txt",
        True:"./api/my_packages/fake_users/jmena/male.txt",
        "surname":"./api/my_packages/fake_users/jmena/surname.txt"}
else:
    names = {
        False:"./api/my_packages/fake_users/jmena/male.txt",
        True:"./api/my_packages/fake_users/jmena/male.txt",
        "surname":"./api/my_packages/fake_users/jmena/surname.txt"}

class CzNames:
    def __init__(self,gender = None):
        self.gender = gender
        if self.gender == None:
            self.gender = choice((True,False))
        self.first_name = self.get_first_name()
        self.surname = self.get_surname()

    def get_first_name(self):
        with open (names[self.gender],"r",encoding="utf8") as file:
            name = choice(file.readlines())
        return name.strip()

    def get_surname(self):
        male = []
        female = []
        with open (names["surname"],"r",encoding="utf8") as file:
            for line in file:
                if line.strip().endswith("á"):
                    female.append(line.strip())
                else: 
                    male.append(line.strip())
            if self.gender: 
                return choice(male)
            else: 
                return choice(female)
            