from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from decorators import is_admin
from forms import LoginForm, SignupForm
from helpers import env, is_checked
from models import User

blueprint = Blueprint('login', __name__, template_folder='templates/login')


@blueprint.route("/login", methods=["GET", "POST"])
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


@blueprint.route("/signup", methods=["GET", "POST"])
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
        return redirect(url_for(".login"))
    return render_template("signup.html", form=form)


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for(".login"))