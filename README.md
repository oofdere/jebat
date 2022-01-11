# jebat

## Development setup
1. Install `python3` and `pip3`
2. `cd jebat`
3. optionally activate your venv
4. `pip install -r requirements.txt`
5. `flask run`

## To-do
 - Database
     - SQLite
         - Users
             - ID
             - Username
             - Password (hashed)
         - Images
             - ID
             - Hash
             - Caption
             - EXIF
             - Upload Date
             - User ID
         - Tags
             - ID
             - Name
         - Album
             - ID
             - Name
     - Graph database (later, to make searches faster)
         - Image Hash
             - User ID
             - Tags
             - Albums
             - Other search criteria
     - Flat-file database (read: files in a folder)
         - Images
         - Thumbnails
 - Storage
     - just simple files in a folder
     - `hash.type` filenames
     - `IMAGE_DIR` environment variable
 - Code
     - `app.py` contains flask things and image views
     - `models.py` contains the database models
     - `accounts.py` contains the login and signup views/logic
     - `images.py` contains fucntions to process images