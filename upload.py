import hashlib
import os
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

import thumbnail
from app import db
from decorators import can_upload
from forms import UploadForm
from helpers import env
from models import Image

blueprint = Blueprint("upload", __name__, template_folder="templates/upload")


@blueprint.route("", methods=["GET", "POST"])
@can_upload
def upload():
    form = UploadForm()
    if request.method == "POST":
        if form.validate_on_submit():
            f = form.file.data
            filename = secure_filename(f.filename)
            extension = filename.split(".")[1]
            image_hash = hashlib.md5(f.read()).hexdigest()
            filename = image_hash + "." + extension
            image = Image(
                hash=image_hash,
                extension=extension,
                caption=form.caption.data,
                date=datetime.now(),
                user_id=current_user.id,
            )
            db.session.add(image)
            db.session.commit()
            f.seek(0)
            f.save(os.path.join(blueprint.root_path, env("IMAGE_DIR"), filename))
            thumbnail.create(filename)
            return redirect(url_for("view", image_hash=image_hash))
    else:
        return render_template("upload.html", form=form)
