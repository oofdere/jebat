import sqlalchemy
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager

db = SQLAlchemy()

image_to_album = db.Table('image_to_album',
                          db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
                          db.Column('album_id', db.Integer, db.ForeignKey('album.id'))
                          )

image_tag = db.Table('image_tag',
                     db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )

image_like = db.Table('image_like',
                      db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
                      db.Column('like_id', db.Integer, db.ForeignKey('like.id'))
                      )


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.Text, unique=True, nullable=False)
    extension = db.Column(db.Text)
    caption = db.Column(db.Text)
    exif = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    in_album = db.relationship("Album", secondary=image_to_album, lazy='dynamic', backref='images_in_album')
    tags = db.relationship("Tag", secondary=image_tag, backref='images')
    likes = db.relationship("Like", secondary=image_like, backref='in_image')

    def get_all_likes(self):
        return len(self.likes)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean)
    can_upload = db.Column(db.Boolean)
    can_view = db.Column(db.Boolean)
    uploads = db.relationship("Image", backref="uploader", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text)
    description = db.Column(db.Text)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    namespace = db.Column(db.Text)
    color = db.Column(db.Text)


# thinking of adding a value row which would either be 1 or -1, which would correspond to a like
# or a dislike. then just taking the sum of all likes to get the average rating
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
