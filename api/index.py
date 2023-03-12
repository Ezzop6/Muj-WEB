from flask import Flask
import os
from customtools import *

app = Flask(__name__)

@app.route('/')
def home():
    return "index page"

@app.route('/about/')
def about():
    return 'About'


@app.route('/hello/')
def hello():
    return 'hello'



if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    app.debug = True #TODO remove this after development
    app.jinja_env.globals.update(get_random_produkt_img=get_random_produkt_img)
    app.run(host=host, port=port)