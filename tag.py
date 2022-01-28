from flask import Blueprint, render_template

from helpers import env
from models import Image

blueprint = Blueprint('tag', __name__, template_folder="templates/tag")

from cog.torque import Graph

g = Graph("tags", env("GRAPH_DIR"))

@blueprint.route("<tag>/add/<image_id>")
def add(image_id: str, tag: str):
    # add a tag to an image
    return g.put(str(image_id), "tag", tag)

def images_by_tag(tag: str):
    # takes in a tag,
    # returns a list of images
    query = g.v(tag).inc("tag").all()
    out = []
    for result in query["result"]:
        image = Image.query.filter_by(id=result["id"]).first()
        out.append(image)
    return out

def tags_by_image(image_id: str):
    # takes in an image,
    # returns a list of tags
    query = g.v(image_id).out("tag").all()
    out = []
    for result in query["result"]:
        out.append(result["id"])
    return out

def all_tags():
    query = g.v().out("tag").all()
    out = []
    for result in query["result"]:
        out.append(result["id"])
    return out

@blueprint.route("")
def view_all():
    tags = all_tags()
    print(tags)
    return render_template("tags.html", tags=tags)

@blueprint.route("<tag>")
def view(tag):
    image_ids = images_by_tag(tag)
    return render_template("tag.html", images=image_ids, tag_name=tag)
