import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from app import login_manager

db = SQLAlchemy()


image_to_album = db.Table('image_to_album',
                          db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
                          db.Column('album_id', db.Integer, db.ForeignKey('album.id'))
                          )


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.Text, unique=True, nullable=False)
    extension = db.Column(db.Text)
    caption = db.Column(db.Text)
    exif = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    in_album = db.relationship("Album", secondary=image_to_album, backref='images_in_album')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean)
    can_upload = db.Column(db.Boolean)
    can_view = db.Column(db.Boolean)
    uploads = db.relationship("Image", backref="images", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text)
    description = db.Column(db.Text)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
