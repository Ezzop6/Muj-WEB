from termcolor import colored
from os import listdir
from random import choice, shuffle

def cprint(text, color="light_green"):
    print(colored(text, color))
    
def random_secret_key():
    randon_secret_string = PasswordGenerator(10,10,10).generate_password()
    return randon_secret_string


def get_random_produkt_img(img_path):
    img_list = listdir(f"static/img/products/{img_path}/")
    return f"../static/img/products/{img_path}/{choice(img_list)}"

class PasswordGenerator:
    def __init__(self,small_letters = 3,big_letters = 3,digits = 2,special_character = 4):
        self.character_small = "abcdefghijklmnopqrstuvwxyz"
        self.character_big = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.character_digit = "0123456789"
        self.character_special = "!@#$%^&*()_+"
        self.small_letters = small_letters
        self.big_letters = big_letters
        self.digits = digits
        self.special_character = special_character
        self.generate_password()

 
    def generate_password(self):
        self.password = [ choice(self.character_small) for i in range(self.small_letters)]
        self.password += [ choice(self.character_big) for i in range(self.big_letters)]
        self.password += [ choice(self.character_digit) for i in range(self.digits)]
        self.password += [ choice(self.character_special) for i in range(self.special_character)]
        shuffle(self.password)
        self.password = "".join(self.password)
        return self.password
