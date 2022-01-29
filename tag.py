from termios import PARODD
from flask import Blueprint, render_template

from models import Tag, Image

from app import db

blueprint = Blueprint('tag', __name__, template_folder='templates/tag')

def get(tag_name):
    # finds the id for the given tag.
    # if none, then it makes the tag.
    # returns the requested Tag object.
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
    return tag

@blueprint.route("")
def all():
    all_tags = Tag.query.all()
    return render_template("all_tags.html", tags=all_tags)

@blueprint.route("/<tag_name>")
def view(tag_name):
    pass

@blueprint.route("/<tag_name>/add/<image_id>")
def add(tag_name, image_id):
    # add a tag to an image
    tag = get(tag_name)
    image = Image.query.filter_by(id=image_id).first()
    image.tags.append(tag)
    db.session.commit()
    return render_template("tag_added.html", tag=tag)

@blueprint.route("<tag>/remove/<image_id>")
def remove(tag):
    # remove a tag from an image
    pass

def tags(image_id):
    # return the tags on a given image
    pass

def images(tag_id):
    # return the images for a given tag
    pass