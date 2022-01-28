# for functions that can be used throughout the website
# this also serves as the CLI for managing the application

# cli
import typer

cli = typer.Typer()

# allows for accessing .env variables
import os

from dotenv import load_dotenv

load_dotenv()
def env(key):
    return os.getenv(key)

# checks if checkbox is checked
# html forms return "on" if a checkbox is checked
# and nothing if it isn't
# wonderful
def is_checked(request, name):
    name = request.form.get(name)
    if name == "on":
        return True
    else:
        return False

# compress images for thumbnails
@cli.command()
def generate_thumbnail(image):
    pass

@cli.command()
def initialize():
    typer.echo("Make sure to copy template.env into .env and change the SECRET_KEY before usage.")
    dir = env("IMAGE_DIR")
    typer.echo("Make sure to make an images directory at {dir} before starting the application.")
    typer.echo("Creating database...")
    from app import app, db
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    cli()