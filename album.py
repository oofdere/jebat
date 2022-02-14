from flask import (Blueprint, Markup, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user
from sqlalchemy import desc
from sqlalchemy.util.topological import sort

from app import db
from decorators import can_view
from forms import AlbumForm
from models import Album, Image

blueprint = Blueprint('album', __name__, template_folder='templates/album')


@blueprint.route("")
@can_view
def albums():
    all_albums = Album.query.all()
    print(all_albums)
    return render_template("albums.html", albums=all_albums)


@blueprint.route("/new", methods=["GET", "POST"])
@can_view
def new():
    form = AlbumForm()
    if request.method == "POST":
        print("post request to create album")
        name_of_album = form.name.data
        description_of_album = form.description.data
        new_album = Album(name=name_of_album, description=description_of_album,
                          user_id=current_user.id)
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('album.view', album_id=new_album.id))
    return render_template("create_album.html", form=form)


@blueprint.route("/<int:album_id>", methods=["GET", "POST"])
@can_view
def view(album_id):
    album = Album.query.filter_by(id=album_id).first()
    sort_type = request.args.get('sort_type')
    if sort_type == "old":
        images = Image.query.with_parent(album).order_by(Image.date)
    elif sort_type == "new":
        images = Image.query.with_parent(album).order_by(desc(Image.date))
    else:
        print("sort by popularity")
        images = Image.query.with_parent(album)
    print(images)
    return render_template("album.html", album=album, images=images, sort_type=sort_type)


@blueprint.route("/add/<int:img_id>", methods=["POST"])
@can_view
def add(img_id):
    album_id = request.form['choose_album']
    album = Album.query.filter_by(id=album_id).first()
    image = Image.query.filter_by(id=img_id).first()
    album.images_in_album.append(image)
    db.session.commit()
    all_albums = Album.query.all()
    album_link = url_for('album.view', album_id=album.id)
    flash(Markup(f'Added to <a href="{album_link}">{album.name}</a>'))
    return render_template("album_add_partial.html", albums=all_albums, image=image)
