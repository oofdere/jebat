import os
from datetime import datetime

import flask_login
from sqlalchemy import desc

import thumbnail

from helpers import env, is_checked

from flask import Blueprint, Flask, flash, render_template, redirect, request, send_from_directory, url_for, flash, send_file, abort

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


@app.route("/upload", methods=["GET", "POST"])
@can_upload
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
            thumbnail.create(filename)
            return redirect(url_for('view', image_hash=image_hash))
    else:
        return render_template("upload.html", form=form)


@app.route("/albums")
@can_view
def albums():
    all_albums = Album.query.all()
    print(all_albums)
    return render_template("albums.html", albums=all_albums)


@app.route("/create_album", methods=["GET", "POST"])
@can_view
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
@can_view
def album(album_id):
    get_album = Album.query.filter_by(id=album_id).first()
    album_images = get_album.images_in_album
    return render_template("album.html", album=get_album, album_images=album_images)


@app.route("/album/add/<int:img_id>", methods=["POST"])
@can_view
def add_to_album(img_id):
    album_id = request.form['choose_album']
    album_list = Album.query.filter_by(id=album_id).first()
    get_image = Image.query.filter_by(id=img_id).first()
    album_list.images_in_album.append(get_image)
    db.session.commit()
    return redirect(url_for('album', album_id=album_id))


@app.route("/<image_hash>")
@can_view
def view(image_hash):
    image = Image.query.filter_by(hash=image_hash).first()
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


@app.route("/admin")
@is_admin
def admin():
    user = User.query.filter_by(id=current_user.id).first()
    if user.is_admin:
        return "admin"
    return "not admin"


@app.route("/roles", methods=["GET", "POST"])
@is_admin
def roles():
        if request.method == "POST":
            user_id = request.form['user_id']
            user = User.query.filter_by(id=user_id).first()
            user.is_admin = is_checked(request, "is_admin")
            user.can_upload = is_checked(request, "can_upload")
            user.can_view = is_checked(request, "can_view")
            db.session.add(user)
            db.session.commit()
            return render_template("roles_partial.html", user=user)
        else:
            all_users = User.query.all()
            return render_template("roles.html", all_users=all_users)