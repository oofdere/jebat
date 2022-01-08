from flask import Flask, render_template, request

import db

app = Flask(__name__, static_url_path='')
# static_url_path sets the path static files are served from
# by default it's /static

@app.route("/<name>")
def home(name):
    # show a home page
    # name = request.args.get("name")
    return render_template("home.html", name=name)

@app.route("/upload")
def upload():
    # upload an image into the database
    pass

@app.route("/<int:image_id>")
def view():
    # show a single image
    pass

@app.route("/pool/<int:pool_id>")
def pool():
    # show a collection of images
    pass

@app.route("/search")
def search():
    # search images by tags
    pass
