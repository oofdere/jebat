import os
import contextlib

from flask import Blueprint, redirect, render_template, url_for
from helpers import env

from models import Image, Album

from decorators import can_view

from tag import get_tags, remove

from app import db

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
@can_view
def delete(image_hash):
    image = Image.query.filter_by(hash=image_hash).first()
    # Remove files
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