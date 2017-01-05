# Settings
DEBUG = True  # Security risk: Change to False on production servers.
WHOAMI = 'paced'

UPLOAD_DIR = 'pics'
APIKEY_FILE = 'api.keys'
DATABASE = 'flaskgur.db'
SCHEMA = 'schema.sql'
ENTROPY = 64  # APIkey length.
ALLOWED_EXTENSIONS = ["jpg", "png", "txt", "mp4", "webm", "mp3", "gif", "bmp",
                      "mp4"]

# It's recommended to keep these as is.
PATH_MINLENGTH = 2
PATH_MAXLENGTH = 4

# Total number of collisions before the system tries to increase maxlength.
TOO_MANY_COLLISIONS = 120
