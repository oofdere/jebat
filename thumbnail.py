from PIL import Image
from helpers import env
import os

img_dir = env("IMAGE_DIR")
thumb_dir = env("THUMB_DIR")

def create(imageName: str):
    img = Image.open(img_dir + "/" + imageName)
    width = img.size[0]
    height = img.size[1]
    if (width > height):
        new_width = 500
        new_height = round(500/width * height);
    elif (img.size[1] > img.size[0]):
        new_height = 500
        new_width = round(500/height * width);
    else:
        new_height = 500
        new_width = 500

    
    print(img.size)
    img = img.resize((new_width, new_height))
    print(new_height, new_width)
    img.convert("RGB")
    print(img.size)
    img.save(os.path.join(thumb_dir + "/" + imageName))
