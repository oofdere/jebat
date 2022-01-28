from flask import Blueprint, render_template, request
from flask_login import current_user

from app import db
from decorators import is_admin
from helpers import is_checked
from models import User

blueprint = Blueprint('admin', __name__, template_folder='templates/admin')


@blueprint.route("/")
@is_admin
def admin():
    user = User.query.filter_by(id=current_user.id).first()
    if user.is_admin:
        return "admin"
    return "not admin"


@blueprint.route("/roles", methods=["GET", "POST"])
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
