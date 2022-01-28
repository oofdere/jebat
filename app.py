import os
from datetime import datetime

import flask_login
from sqlalchemy import desc

import thumbnail

from helpers import env, is_checked

from flask import Blueprint, Flask, flash, render_template, redirect, request, send_from_directory, url_for, flash, \
    send_file, abort, Markup

from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename

app = Flask(__name__)
# static_url_path sets the path static files are served from
# by default it's /static
app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = env("SECRET_KEY")
login = LoginManager(app)
login.login_view = "login"
from models import *

db.init_app(app)

from flask_migrate import Migrate

migrate = Migrate(app, db)

from forms import *
import hashlib

from decorators import *


@app.route("/")
@login_required
def home():
    images = Image.query.order_by(desc(Image.date)).all()
    return render_template("recent.html", images=images)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return "Invalid username or password"
        login_user(user, remember=form.remember.data)
        return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            is_admin=bool(env("IS_ADMIN")),
            can_view=bool(env("CAN_VIEW")),
            can_upload=bool(env("CAN_UPLOAD"))
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Signup successful.")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/<image_hash>")
@can_view
def view(image_hash):
    image = Image.query.filter_by(hash=image_hash).first()
    print(image)
    all_albums = Album.query.all()
    return render_template("detail_view.html", image=image, albums=all_albums)


@app.route("/pool/<int:pool_id>")
@can_view
def pool(pool_id):
    # show a collection of images
    pass


@app.route("/thumbnails/<filename>")
def get_thumb(filename):
    filepath = os.path.join(app.root_path, env("THUMB_DIR"), secure_filename(filename))
    return send_file(filepath, mimetype='image/jpeg')


@app.route("/search")
def search():
    # search images by tags
    pass


blueprint = Blueprint('images', __name__, static_url_path='/images', static_folder='images/')
app.register_blueprint(blueprint)

import admin, upload, album

app.register_blueprint(admin.blueprint, url_prefix='/admin')
app.register_blueprint(upload.blueprint, url_prefix='/upload')
app.register_blueprint(album.blueprint, url_prefix='/album')
