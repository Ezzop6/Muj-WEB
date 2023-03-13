from flask import Flask
import os

from api._tools import *
from api.routes import bl_main_pages

app = Flask(__name__)
app.register_blueprint(bl_main_pages, url_prefix='/')



if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    # app.debug = True #TODO remove this after development
    app.jinja_env.globals.update(get_random_produkt_img=get_random_produkt_img)
    app.run(host=host, port=port)