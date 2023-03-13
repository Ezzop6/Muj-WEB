debug = False #pred načítaním na server nastavit na False nemam paru proc

if debug:
    from my_packages._tools import *
    from bl_pages.main_pages import main_pages
else:
    from api.my_packages._tools import *
    from api.bl_pages.main_pages import main_pages


from flask import Flask
import os

main = main_pages

app = Flask(__name__)
app.register_blueprint(main, url_prefix='/')



if __name__ == '__main__':
    if debug:
        app.debug = True
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    app.jinja_env.globals.update(get_random_produkt_img=get_random_produkt_img)
    app.run(host=host, port=port)