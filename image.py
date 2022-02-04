import contextlib
import os

from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import fresh_login_required

from app import db
from decorators import can_view
from helpers import env
from account import is_owner
from models import Album, Image
from tag import get_tags, remove

blueprint = Blueprint('image', __name__, template_folder='templates/image')

@blueprint.route("<image_hash>")
@can_view
def view(image_hash):
    image = Image.query.filter_by(hash=image_hash).first()
    print(image)
    all_albums = Album.query.all()
    tags = get_tags(image.id)
    return render_template("detail_view.html", image=image, albums=all_albums, tags=tags)

@blueprint.route("<image_hash>/delete", methods=["POST"])
@fresh_login_required
def delete(image_hash):
    image = Image.query.filter_by(hash=image_hash).first()
    # Remove files
    if is_owner(image):    
        filename = image.hash + "." + image.extension
        with contextlib.suppress(FileNotFoundError):
            os.remove(os.path.join(blueprint.root_path, env("IMAGE_DIR"), filename))
            os.remove(os.path.join(blueprint.root_path, env("THUMB_DIR"), filename))
        # Remove from tags
        for tag in image.tags:
            remove(tag.namespace, tag.name, image.id)
        db.session.delete(image)
        db.session.commit()
        return(redirect(url_for('home')))
    else:
        return abort(403)
