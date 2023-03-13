from flask import Flask
import os
from api._tools import *
from routes import modul

app = Flask(__name__)
app.register_blueprint(modul, url_prefix='/')




if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    app.debug = True #TODO remove this after development
    app.jinja_env.globals.update(get_random_produkt_img=get_random_produkt_img)
    app.run(host=host, port=port)