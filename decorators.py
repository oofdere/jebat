from functools import wraps

from flask import abort, g, redirect, request, url_for
from flask_login import current_user

from models import User


# decorators to apply scopes to routes
def can_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated == False:
            return redirect(url_for("login.login"))
        user = User.query.filter_by(id=current_user.id).first()
        if user.can_view:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function

def can_upload(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated == False:
            return redirect(url_for("login.login"))
        user = User.query.filter_by(id=current_user.id).first()
        if user.can_upload:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated == False:
            return redirect(url_for("login.login"))
        user = User.query.filter_by(id=current_user.id).first()
        if user.is_admin:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function