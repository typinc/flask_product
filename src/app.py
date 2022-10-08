import localconfig
from models import db, Desktop, Laptop, Image, ImageView

from os.path import exists

import sqlite3
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def get_db_connection():
    conn = sqlite3.connect(localconfig.SQLALCHEMY_DATABASE_URI)
    conn.row_factory = sqlite3.Row
    return conn


def get_product_information(db_table: str) -> list[dict]:
    conn = get_db_connection()
    db_product = conn.execute(f'SELECT * FROM {db_table};').fetchall()
    conn.close()
    items = []
    for its in db_product:
        its = dict(its)
        its['image_name'] = localconfig.UPLOAD_FOLDER + its['image_name']
        items.append(its)
    return items


flaskapp = Flask(__name__)

flaskapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + localconfig.SQLALCHEMY_DATABASE_URI
flaskapp.config['SECRET_KEY'] = 'mysecret'


@flaskapp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@flaskapp.route("/")
def index():
    return render_template('index.html')


@flaskapp.route("/laptop")
def laptop():
    laptops = get_product_information('laptop')
    return render_template('laptop.html', laptops=laptops)


@flaskapp.route("/develop")
def develop():
    return render_template('develop.html')


if __name__ == "__main__":
    db.app = flaskapp
    db.init_app(flaskapp)
    admin = Admin(flaskapp, template_mode='bootstrap4')
    admin.add_view(ModelView(Desktop, db.session))
    admin.add_view(ModelView(Laptop, db.session))
    admin.add_view(ImageView(Image, db.session))
    if not exists(localconfig.SQLALCHEMY_DATABASE_URI):
        db.create_all()
    flaskapp.run(host='0.0.0.0', debug=True)
