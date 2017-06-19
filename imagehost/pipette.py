"""pipette imagehost module main script file for utils and server ops."""
import os
import random
import sqlite3
import string
from os.path import isfile, join, splitext
from sys import argv

from flask import Flask, abort, render_template, request, send_from_directory
from werkzeug import secure_filename

import yaml
from flask_compressor import Compressor, CSSBundle, FileAsset
from flask_htmlmin import HTMLMIN as htmlmin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils import *

# These settings are not necessary to not hardcode:
UPLOAD_DIR = 'pics'
DATABASE = 'pipette.db'
SCHEMA = 'schema.sql'
TOO_MANY_COLLISIONS = 50

# Get information from our YAML file:
with open('settings.yaml') as f:
    settings = yaml.load(f.read())

    DEBUG = dictSet(settings, 'DEBUG')
    STASH = dictSet(settings, 'STASH')
    WHOAMI = dictSet(settings, 'WHOAMI')
    BASE_DESCRIPTION = dictSet(settings, 'BASE_DESCRIPTION')
    DIAG_DESCRIPTION = dictSet(settings, 'DIAG_DESCRIPTION')
    ALLOWED_EXTENSIONS = set(dictSet(settings, 'ALLOWED_EXTENSIONS'))
    PATH_MINLENGTH = dictSet(settings, 'PATH_MINLENGTH')
    PATH_MAXLENGTH = dictSet(settings, 'PATH_MAXLENGTH')
    INSEC_MINLENGTH = dictSet(settings, 'INSEC_MINLENGTH')
    INSEC_MAXLENGTH = dictSet(settings, 'INSEC_MAXLENGTH')


app = Flask(__name__)
app.config.from_object(__name__)
app.config['MINIFY_PAGE'] = not DEBUG

# Rate limit default settings
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=["3600 per hour"]
)

# Minification
htmlmin(app)
compressor = Compressor()
compressor.init_app(app)

# Bundles to be compressed
raleway = FileAsset(filename='css/raleway.css', processors=['cssmin'])
skeleton = FileAsset(filename='css/skeleton.css', processors=['cssmin'])
customcss = FileAsset(filename='css/custom.css', processors=['cssmin'])

cssBundle = CSSBundle('allCSS', assets=[raleway, skeleton, customcss],
                      processors=['cssmin'])
compressor.register_bundle(cssBundle)


def getNoTaken(ext):
    """Check the number of files with an extension in the database."""
    db = sqlite3.connect(DATABASE)
    picNo = db.execute('SELECT COUNT(1) FROM Pics WHERE filename ' +
                       'LIKE ?', ('%' + ext,))

    picNoResp = int(picNo.fetchall()[0][0])
    db.close()
    return picNoResp


def databaseFull():
    """Check whether a database is full."""
    db = sqlite3.connect(DATABASE)
    picNo = db.execute('SELECT COUNT(filename) FROM `Pics` GROUP BY `id`')

    returnVal = True if int(picNo[0]) >= getMaxPossible() else False
    db.close()
    return returnVal


def hash(size):
    """Insecurely generate a random string of n size."""
    chooseFrom = string.ascii_uppercase + string.ascii_lowercase + \
        string.digits
    chars = [random.SystemRandom().choice(chooseFrom) for _ in range(size)]

    return str(''.join(chars))


def okApiKey(apikey, verbose=DEBUG):
    """Return True if API key is accepted."""
    open('api.keys', 'a').close()  # Touch file if it doesn't exist.
    with open('api.keys', 'r') as f:
        if verbose:
            print("\nYour API key is: '" + apikey + "'\n")
        for j in [str(i.rstrip()) for i in f.readlines()]:
            if verbose:
                print("Testing: " + j)
            if j == apikey.rstrip():
                if verbose:
                    print("Okay API key!")
                return True
        if verbose:
            print("API key not in list! Failed.")
        return False


def allowedExtension(extension):
    """Make sure extension is in the ALLOWED_EXTENSIONS set."""
    return extension in ALLOWED_EXTENSIONS


def isUnique(filename, verbose=DEBUG):
    """Check if a filename exists in the database."""
    db = sqlite3.connect(DATABASE)
    items = db.execute('SELECT filename FROM `Pics` WHERE filename LIKE (?)',
                       (filename, ))

    if filename in items:
        db.close()
        if verbose:
            print(filename + " was taken!")
        return False

    db.close()
    if verbose:
        print(filename + " was not taken!")
    return True


def addPic(filename):
    """Insert filename into database."""
    db = sqlite3.connect(DATABASE)
    r = db.execute('INSERT INTO `Pics` (filename) VALUES (?)', (filename, ))
    db.commit()
    db.close()

    return r


def init():
    """(Re)initialise database file."""
    db = sqlite3.connect(DATABASE)
    with app.open_resource(SCHEMA, mode='r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()


@app.errorhandler(502)
def fiveOhTwo(e):
    """View for 502 page."""
    return render_template('502.html'), 502


@app.errorhandler(500)
def internalServerError(e):
    """View for 502 page."""
    return render_template('500.html'), 500


@app.errorhandler(404)
def notFound(e):
    """View for 404 page."""
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    """View for 403 page."""
    return render_template('403.html'), 403


@app.route('/', methods=['GET', 'POST'])
def uploadPic():
    """Root image host."""
    if request.method == 'POST':
        file = request.files['file']
        apikey = str(request.form['apikey']).rstrip()
        extension = str(splitext(file.filename)[1].lower()[1:])

        if file and okApiKey(apikey) and allowedExtension(extension) or DEBUG:
            gettingFullWarning = False
            counter = 0
            extension = "." + extension

            # Check secure settings for URL length.
            if 'insecure' in request.form:
                # Don't rely on short circuiting.
                if str(request.form['insecure']).lower() in ('1', 'true',
                                                             'yes'):
                    minlength = INSEC_MINLENGTH
                    maxlength = INSEC_MAXLENGTH
                else:
                    minlength = PATH_MINLENGTH
                    maxlength = PATH_MAXLENGTH
            else:
                minlength = PATH_MINLENGTH
                maxlength = PATH_MAXLENGTH

            while True:
                fn = hash(random.randint(minlength, maxlength))

                # Check that we're not getting too full.
                if counter >= TOO_MANY_COLLISIONS:
                    if not gettingFullWarning:
                        print("We are adding a file to a densely " +
                              "populated database. We will start to " +
                              "accept collisions once we're full.")
                        gettingFullWarning = True
                    elif databaseFull():
                        return 500

                # Check that fn doesn't already exist in the database.
                if isUnique(fn):
                    break

                counter -= 1

            # This will overwrite existing if required.
            dirExists(UPLOAD_DIR)
            file.save(join(UPLOAD_DIR, fn + extension))

            # Finally, add the URL to the db table.
            addPic(fn + extension)

            return request.url_root + fn + extension

        # Bad file extension, no file, or bad API key.
        abort(403)

    # If the user just tries to get to the site without a POST request:
    return render_template('base.html', hostname=request.url_root, me=WHOAMI,
                           desc=BASE_DESCRIPTION)


@app.route('/delete/<filename>', methods=["POST"])
def delete(filename):
    """If a correct POST request is sent with apikey, deletes a file."""
    apikey = str(request.form['apikey']).rstrip()

    # First check API key.
    if not okApiKey(apikey):
        return "Forbidden. Bad API key.", 403

    # Don't delete from the database. Just let it 404. Imagine sending
    # something and the recipient, down the line, stumbling upon it only for
    # it to be something completely different.

    # Test if the file exists.
    if not os.path.exists(os.path.join(UPLOAD_DIR, filename)):
        return "Nothing to do. File not found.", 404

    # Now, depending on our settings file, we either delete the file or stash.
    if STASH:
        os.rename(os.path.join(UPLOAD_DIR, filename),
                  os.path.join(UPLOAD_DIR, 'stash/' + filename))
    else:
        os.remove(os.path.join(UPLOAD_DIR, filename))

    return "Success. No longer exists: " + request.url_root + filename, 202


@app.route('/diagnostics/')
def diagnostics():
    """Diagnostic view."""
    filesUsed = list()  # List of dicts with data to be passed to template.
    totalUsed = 0  # Cumulative sum of the total used files.

    for i in ALLOWED_EXTENSIONS:
        taken = getNoTaken(i)
        totalUsed += taken

        if taken == 0:
            continue

        filesUsed.append({"extension": i, "used": '{:,}'.format(taken)})

    # Now, sort the files used so the type with the highest usage is first.
    filesUsed = sorted(filesUsed, reverse=True, key=lambda k: int(k['used']))

    # Total calculations.
    filesUsed.append({"extension": "TOTAL", "used": '{:,}'.format(totalUsed)})

    # We also pass the size of the pics directory to diagnostics.
    dirSize = getDirSize(UPLOAD_DIR)

    return render_template('diagnostics.html', payload=filesUsed, me=WHOAMI,
                           desc=DIAG_DESCRIPTION, dirSize=dirSize)


@app.route("/admin/")
def auth():
    """Authenticate user and provide admin controls."""
    return "Not yet implemented."


@app.route('/<filename>')
def returnPic(filename):
    """Fetch the image from the URL."""
    return send_from_directory(app.config['UPLOAD_DIR'],
                               secure_filename(filename))


@app.route('/favicon.ico')
def favicon():
    """Legacy favicon."""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicons/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    # If run with no cmdline args, just start the server.

    # Ensure database is initialised.
    if not isfile(DATABASE):
        with open(DATABASE, 'a') as f:
            init()

    """ Operations:
    - start: start pipette server.
    - newkey: generate new API key.
    - checkkey: verbosely checks if an API key is good.
    - checkunique: check if a filename is unique.
    - restart: destroys all file references in database.
    """

    if len(argv) == 1:
        app.run(debug=DEBUG, host='0.0.0.0')
    elif len(argv) >= 2:
        if argv[1].lower() in ["start", "run", "runserver"]:
            app.run(debug=DEBUG, host='0.0.0.0')
        elif argv[1].lower() == "newkey":
            print("Your secret API key is: " + addApiKey())
        elif argv[1].lower() == "checkkey":
            print("Checking that your key is valid...")
            okApiKey(argv[2], True)
        elif argv[1].lower() == "checkunique":
            print("Checking that your key is unique...")
            isUnique(argv[2], True)
        elif argv[1] == "restart":
            if raw_input("Are you ABSOLUTELY sure? All files will be " +
                         "destroyed! Type 'yes' if you understand. ") == "yes":
                init()
                print("Restarted! Old files have not been purged.")
            else:
                print("Nothing was changed.")
        else:
            print("Your command was not recognised: " + argv[1:].join(" "))
