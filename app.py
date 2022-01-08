from flask import Flask, render_template, request

import db

app = Flask(__name__, static_url_path='')
# static_url_path sets the path static files are served from
# by default it's /static

@app.route("/")
def home():
    # show a home page
    pass

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
