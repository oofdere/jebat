from flask import Blueprint, render_template

from models import Image, Album

from decorators import can_view

from tag import get_tags

blueprint = Blueprint('image', __name__, template_folder='templates/image')

@blueprint.route("<image_hash>")
@can_view
def view(image_hash):
    image = Image.query.filter_by(hash=image_hash).first()
    print(image)
    all_albums = Album.query.all()
    tags = get_tags(image.id)
    return render_template("detail_view.html", image=image, albums=all_albums, tags=tags)