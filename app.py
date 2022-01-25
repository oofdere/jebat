import os
from datetime import datetime

import flask_login
from sqlalchemy import desc

from helpers import env

from flask import Blueprint, Flask, flash, render_template, redirect, request, send_from_directory, url_for, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename

app = Flask(__name__)
# static_url_path sets the path static files are served from
# by default it's /static
# app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
# app.config["SECRET_KEY"] = env("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SECRET_KEY"] = "fortnite"
login = LoginManager(app)
login.login_view = "login"
from models import *

db.init_app(app)
from forms import *
import hashlib


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
        user = User(username=form.username.data)
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


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = UploadForm()
    if request.method == "POST":
        if form.validate_on_submit():
            f = form.file.data
            filename = secure_filename(f.filename)
            extension = filename.split('.')[1]
            image_hash = hashlib.md5(f.read()).hexdigest()
            filename = image_hash + "." + extension
            image = Image(hash=image_hash, extension=extension, caption=form.caption.data,
                          date=datetime.now(), user_id=current_user.id)
            db.session.add(image)
            db.session.commit()
            f.seek(0)
            f.save(os.path.join(app.root_path, env("IMAGE_DIR"), filename))
            return redirect(url_for('view', image_hash=image_hash))
    else:
        return render_template("upload.html", form=form)


@app.route("/albums")
def albums():
    all_albums = Album.query.all()
    print(all_albums)
    return render_template("albums.html", albums=all_albums)


@app.route("/create_album", methods=["GET", "POST"])
@login_required
def create_album():
    form = AlbumForm()
    if request.method == "POST":
        print("post request to create album")
        name_of_album = form.name.data
        description_of_album = form.description.data
        new_album = Album(name=name_of_album, description=description_of_album,
                          user_id=current_user.id)
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('album', album_id=new_album.id))
    return render_template("create_album.html", form=form)


@app.route("/album/<int:album_id>", methods=["GET", "POST"])
@login_required
def album(album_id):
    get_album = Album.query.filter_by(id=album_id).first()
    al_images = get_album.images_in_album
    return render_template("album.html", album=get_album, al_images=al_images)


@app.route("/album/add/<int:img_id>", methods=["POST"])
@login_required
def add_to_album(img_id):
    album_id = request.form['choose_album']
    album_list = Album.query.filter_by(id=album_id).first()
    get_image = Image.query.filter_by(id=img_id).first()
    album_list.images_in_album.append(get_image)
    db.session.commit()
    return redirect(url_for('album', album_id=album_id))


@app.route("/<image_hash>")
def view(image_hash):
    image = Image.query.filter_by(hash=image_hash).first()
    all_albums = Album.query.all()
    return render_template("detail_view.html", image=image, albums=all_albums)


@app.route("/pool/<int:pool_id>")
def pool(pool_id):
    # show a collection of images
    pass


@app.route("/search")
def search():
    # search images by tags
    pass


blueprint = Blueprint('images', __name__, static_url_path='/images', static_folder='images/')
app.register_blueprint(blueprint)
