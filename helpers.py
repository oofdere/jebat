# for functions that can be used throughout the website

# allows for accessing .env variables
import os
from dotenv import load_dotenv
load_dotenv()
def env(key):
    return os.getenv(key)

# compress images for thumbnails
def compress(image):
    pass