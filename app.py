import os
from urllib import response

from flask import Blueprint, Flask, render_template, send_file
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException

from helpers import env

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = env("SECRET_KEY")

login_manager = LoginManager(app)
login_manager.login_view = "login.login"

csrf = CSRFProtect(app)

from flask_migrate import Migrate

from models import *

db.init_app(app)
migrate = Migrate(app, db)

import admin
import album
import account
import upload
import image
import tag
from decorators import *

app.register_blueprint(admin.blueprint, url_prefix='/admin')
app.register_blueprint(upload.blueprint, url_prefix='/upload')
app.register_blueprint(album.blueprint, url_prefix='/album')
app.register_blueprint(image.blueprint, url_prefix='/image')
app.register_blueprint(tag.blueprint, url_prefix='/tag')
app.register_blueprint(account.blueprint, url_prefix='/')


@app.route("/")
@login_required
def home():
    images = Image.query.order_by(desc(Image.date)).all()
    return render_template("recent.html", images=images)


@app.route("/pool/<int:pool_id>")
@can_view
def pool(pool_id):
    # show a collection of images
    pass


@app.route("/thumbnails/<filename>")
@can_view
def get_thumb(filename):
    filepath = os.path.join(app.root_path, env("THUMB_DIR"), secure_filename(filename))
    return send_file(filepath, mimetype='image/jpeg')

@app.route("/images/<filename>")
@can_view
def get_image(filename):
    filepath = os.path.join(app.root_path, env("IMAGE_DIR"), secure_filename(filename))
    return send_file(filepath)

blueprint = Blueprint('images', __name__, static_url_path='/images', static_folder='images/')
app.register_blueprint(blueprint)


@app.errorhandler(HTTPException)
def handle_exception(error):
    response = error.get_response()
    return render_template("error.html", error=error, response=response), error.code