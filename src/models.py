from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from flask_admin.contrib import sqla
from flask_admin import form
from flask import url_for
from markupsafe import Markup
import os

import localconfig

db = SQLAlchemy()


class Desktop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    gpu = db.Column(db.String(30))
    cpu = db.Column(db.String(30))
    memory = db.Column(db.String(30))
    storage = db.Column(db.String(30))
    os = db.Column(db.String(30))
    image_name = db.Column(db.String(100))


class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    gpu = db.Column(db.String(30))
    cpu = db.Column(db.String(30))
    memory = db.Column(db.String(30))
    storage = db.Column(db.String(30))
    os = db.Column(db.String(30))
    resolution = db.Column(db.String(30))
    image_name = db.Column(db.String(100))


file_path = os.path.join(os.path.dirname(__file__), 'static/uploads')
try:
    os.mkdir(file_path)
except OSError:
    pass


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name


@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(os.path.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(os.path.join(file_path, form.thumbgen_filename(target.path)))
        except OSError:
            pass


class ImageView(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        return Markup('<img src="%s">' % url_for('static', filename=localconfig.UPLOAD_FOLDER + form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image', base_path=file_path, thumbnail_size=(100, 100, True))
    }
