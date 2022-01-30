import hashlib
from flask import Blueprint, render_template, request
from sqlalchemy import and_, or_

from models import Tag, Image

from app import db

from sqlalchemy.sql import text

blueprint = Blueprint('tag', __name__, template_folder='templates/tag')

def get(tag_name):
    # finds the id for the given tag.
    # if none, then it makes the tag.
    # returns the requested Tag object.
    namespace, tag_name = get_namespace(tag_name)
    tag = Tag.query.filter_by(name=tag_name, namespace=namespace).first()
    if not tag:
        tag = Tag(name=tag_name, namespace=namespace)
        db.session.add(tag)
        db.session.commit()
    return tag

def get_namespace(tag_name):
    if ':' in tag_name:
        namespace, tag_name = tag_name.split(':')
    else:
        namespace = None
    return namespace, tag_name

@blueprint.app_template_global(name="tag_string")
def tag_string(tag):
    if tag.namespace == None:
        return tag.name
    else:
        return tag.namespace + ":" + tag.name

@blueprint.app_template_global(name="color_from_tag")
def color_from_tag(tag):
    if tag.namespace == None:
        return "#1095c1"
    else:
        hash = hashlib.md5(tag.namespace.encode('utf8')).hexdigest()[::6]
        return "#" + hash

def clear(tag):
    if not tag.images:
        db.session.delete(tag)
        db.session.commit()

@blueprint.route("")
def tags():
    all_tags = Tag.query.order_by(Tag.namespace).all()
    print(all_tags)
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

@blueprint.route("<namespace>:<tag_name>/remove/<image_id>")
@blueprint.route("<tag_name>/remove/<image_id>", defaults={'namespace': None})
def remove(namespace, tag_name, image_id):
    image = Image.query.filter_by(id=image_id).first()
    tag = Tag.query.filter_by(name=tag_name, namespace=namespace).first()
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
    namespace, tag_name = get_namespace(tag_name)
    tag = Tag.query.filter_by(name=tag_name, namespace=namespace).first()
    return tag.images