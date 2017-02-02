# Settings
DEBUG = False  # Security risk: Change to False on production servers.
WHOAMI = 'paced'
BASE_DESCRIPTION = 'This is a filehost running on the Python pipette module: a fast, open-source, lightweight, scalable private filehost developed by paced.'
DIAG_DESCRIPTION = 'Diagnostics/usage page for a filehost running on the Python pipette module: a fast, open-source, lightweight, scalable private filehost developed by paced.'

UPLOAD_DIR = 'pics'
APIKEY_FILE = 'api.keys'
DATABASE = 'pipette.db'
SCHEMA = 'schema.sql'
ENTROPY = 64  # APIkey length.
ALLOWED_EXTENSIONS = ["jpg", "png", "txt", "mp4", "webm", "mp3", "gif", "bmp"]

# It's recommended to keep these as is.
PATH_MINLENGTH = 2
PATH_MAXLENGTH = 4

# Total number of collisions before the system tries to increase maxlength.
TOO_MANY_COLLISIONS = 100
