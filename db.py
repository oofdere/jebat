import sqlite3

def add(image: dict):
    # add an image to the database
    # returns image_id if successful
    pass

async def image(image_id: int):
    # query the database for a specific image
    # returns dict of image
    pass

async def page(page_number: int, quantity: int, tags: list):
    # query the database for a collection of images
    # returns a list of image dicts
    pass


