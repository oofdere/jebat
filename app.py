import os
from helpers import env

from flask import Flask, flash, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='')
# static_url_path sets the path static files are served from
# by default it's /static
app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = env("SECRET_KEY")

login = LoginManager(app)
login.login_view = "login"
from models import *
db.init_app(app)
from forms import *

@app.route("/")
@login_required
def home():
    # show a home page
    return render_template("home.html")

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
            f.save(os.path.join(app.root_path, env("IMAGE_DIR"), filename))
            return "done"
    else:
        return render_template("upload.html", form=form)

@app.route("/<int:image_id>")
def view():
    # show a single image
    pass

@app.route("/pool/<int:pool_id>")
def pool():
    # show a collection of images
    pass

@app.route("/search")
def search():
    # search images by tags
    pass

