from flask import Blueprint, render_template, request

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

def clear(tag):
    if not tag.images:
        db.session.delete(tag)
        db.session.commit()

@blueprint.route("")
def tags():
    all_tags = Tag.query.all()
    return render_template("all_tags.html", tags=all_tags)

@blueprint.route("/<tag_name>")
def view(tag_name):
    images = get_images(tag_name)
    return render_template("recent.html", images=images)

@blueprint.route("/add", methods=["POST"])
def add():
    # add a tag to an image
    tag_name = request.form['tag']
    tag = get(tag_name)
    image_id = request.form['image_id']
    image = Image.query.filter_by(id=image_id).first()
    image.tags.append(tag)
    db.session.commit()
    return render_template("tag_list.html", tags=get_tags(image_id), image=image)

@blueprint.route("<tag_name>/remove/<image_id>")
def remove(tag_name, image_id):
    image = Image.query.filter_by(id=image_id).first()
    tag = Tag.query.filter_by(name=tag_name).first()
    image.tags.remove(tag)
    db.session.commit()
    clear(tag)
    return render_template("tag_list.html", tags=get_tags(image_id), image=image)

@blueprint.route("image/<image_id>")
def get_tags(image_id):
    # return the tags on a given image
    image = Image.query.filter_by(id=image_id).first()
    return image.tags


def get_images(tag_name):
    # return the images for a given tag
    tag = Tag.query.filter_by(name=tag_name).first()
    return tag.images