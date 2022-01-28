import os

from flask import Blueprint, Flask, render_template, send_file
from flask_login import LoginManager, login_required
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from helpers import env

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = env("SECRET_KEY")

login_manager = LoginManager(app)
login_manager.login_view = "login.login"

from flask_migrate import Migrate

from models import *

db.init_app(app)
migrate = Migrate(app, db)

from decorators import *

import admin, album, login, upload

app.register_blueprint(admin.blueprint, url_prefix='/admin')
app.register_blueprint(upload.blueprint, url_prefix='/upload')
app.register_blueprint(album.blueprint, url_prefix='/album')
app.register_blueprint(login.blueprint, url_prefix='/')


@app.route("/")
@login_required
def home():
    images = Image.query.order_by(desc(Image.date)).all()
    return render_template("recent.html", images=images)


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


blueprint = Blueprint('images', __name__, static_url_path='/images', static_folder='images/')
app.register_blueprint(blueprint)


