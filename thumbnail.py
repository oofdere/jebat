from PIL import Image
from helpers import env
import os

img_dir = env("IMAGE_DIR")
thumb_dir = env("THUMB_DIR")

def create(imageName: str):
    img = Image.open(img_dir + "/" + imageName)
    
    if (img.size[0] > img.size[1]):
        new_width = 500
        new_height = round(500/img.size[0] * img.size[1]); #new width/old width= scale factor. scale factor * old height = new height
    elif (img.size[1] > img.size[0]):
        new_height = 500
        new_width = round(500/img.size[1] * img.size[0]);
    else:
        new_height = 500
        new_width = 500

    img.thumbnail((new_height, new_width))
    img.convert("RGB")
    img.save(os.path.join(thumb_dir + "/" + imageName))
