from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='')
# static_url_path sets the path static files are served from
# by default it's /static

@app.route("/")
def hello():
    name = request.args.get("name")
    #i.e. example.com/?name=aname
    return render_template("home.html", name=name)
    # the first name is the name variable in the template,
    # which we're assigning the value of the second name, which we just defined.