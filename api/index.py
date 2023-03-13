debug = False #TODO remove this after development

if debug:
    from my_packages._tools import *
    from bl_pages.main_pages import main_pages
else:
    from api.my_packages._tools import *
    from api.bl_pages.main_pages import main_pages


from flask import Flask
import os

bl_main_pages = main_pages

app = Flask(__name__)
app.register_blueprint(bl_main_pages, url_prefix='/')



if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    if debug:
        app.debug = True
    app.jinja_env.globals.update(get_random_produkt_img=get_random_produkt_img)
    app.run(host=host, port=port)