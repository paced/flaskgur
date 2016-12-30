#!/usr/bin/python
from flask import Flask, request, g, redirect, url_for, abort, \
                  render_template, send_from_directory
from werkzeug import secure_filename
from os.path import splitext, join, isfile
from sys import argv

import random
import sqlite3
import os
import string

# Settings
DEBUG = True
SERVER = "https://i.paced.me/"  # Replace this. You must include the slash.
UPLOAD_DIR = 'pics'
APIKEY_FILE = 'api.keys'
DATABASE = 'flaskgur.db'
SCHEMA = 'schema.sql'
ENTROPY = 64  # APIkey length.
ALLOWED_EXTENSIONS = [".jpg", ".png", ".ico", ".bmp", ".txt", ".md", ".gifv",
                      ".mp4", ".gif", ".webm", ".mp3", ".xml", ".json", ".csv"]

# The number of unique images: the sum from s=PATH_MAXLENGTH to PATH_MINLENGTH
# of 61**s where PATH_MINLENGTH subtracted from PATH_MAXLENGTH >= 0. The
# default settings of 2 and 4 respectively allow 14,076,543 of each filetype.
PATH_MINLENGTH = 2
PATH_MAXLENGTH = 4

# Total number of collisions before the system tries to increase maxlength.
TOO_MANY_COLLISIONS = 120

app = Flask(__name__)
app.config.from_object(__name__)


def getMaxPossible():
    """Get the total possible number of combinations."""

    return sum([61**s for s in range(PATH_MINLENGTH, PATH_MAXLENGTH)])


def databaseFull():
    """Check whether a database is full."""

    db = sqlite3.connect(DATABASE)
    picNo = db.execute('SELECT COUNT(filename) FROM `Pics` GROUP BY `id`')

    return True if int(picNo[0]) >= getMaxPossible() else return False


def hash(size):
    """Insecurely generates a random string of n size."""

    chooseFrom = string.ascii_uppercase + string.ascii_lowercase + \
                 string.digits
    chars = [random.SystemRandom().choice(chooseFrom) for _ in range(size)]

    return str(''.join(chars))


def addApiKey():
    """Adds an API key to the api.keys file."""

    with open(APIKEY_FILE, "a") as f:
        key = hash(ENTROPY)
        f.write(key + '\n')

        return key


def okApiKey(apikey):
    """Returns True if API key is accepted."""

    open(APIKEY_FILE, 'a').close()
    with open(APIKEY_FILE, 'r') as f:
        if apikey in [i.rstrip() for i in f.readlines()]:
            return True
        return False


def allowedExtension(extension):
    """Make sure extension is in the ALLOWED_EXTENSIONS set."""

    return extension in ALLOWED_EXTENSIONS


def isUnique(filename):
    """Checks if a filename exists in the database."""

    db = sqlite3.connect(DATABASE)
    items = db.execute('SELECT filename FROM `Pics` WHERE filename == (?)',
                       [filename])

    if filename in items:
        db.close()
        return False

    db.close()
    return True


def addPic(filename):
    """Insert filename into database."""

    db = sqlite3.connect(DATABASE)
    db.execute('INSERT INTO `Pics` (filename) values (?)', [filename])
    db.commit()
    db.close()


def init():
    """(Re)initialises database file."""

    db = sqlite3.connect(DATABASE)
    with app.open_resource(SCHEMA, mode='r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()


@app.errorhandler(503)
def forbidden(e):
    return render_template('502.html'), 502


@app.errorhandler(500)
def forbidden(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def notFound(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.route('/', methods=['GET', 'POST'])
def uploadPic():
    if request.method == 'POST':
        file = request.files['file']
        apikey = request.form['apikey'].rstrip()
        extension = str(splitext(file.filename)[1].lower())

        if file and okApiKey(apikey) and allowedExtension(extension):
            gettingFullWarning = False
            counter = 0
            while True:
                fn = hash(random.randint(PATH_MINLENGTH, PATH_MAXLENGTH))

                # Check that we're not getting too full.
                if counter >= TOO_MANY_COLLISIONS:
                    if not gettingFullWarning:
                        print("We are adding a file to a densely " + \
                              "populated database. We will start to " + \
                              "accept collisions once we're full.")
                    elif databaseFull():
                        break
                    gettingFullWarning = True

                # Check that fn doesn't already exist in the database.
                if isUnique(fn):
                    break

                counter -= 1

            file.save(join(UPLOAD_DIR, fn + extension))

            # Finally, add the URL to the db table.
            addPic(fn)

            return SERVER + fn + extension

        # Bad file extension or API key.
        abort(403)

    # If the user just tries to get to the site without a POST request:
    return render_template('base.html')


@app.route('/<filename>')
def returnPic(filename):
    """Displays the image requested, 404 if not found."""

    return send_from_directory(app.config['UPLOAD_DIR'],
                               secure_filename(filename))


if __name__ == '__main__':
    # If run with no cmdline args, just start the server.

    # Ensure database is initialised.
    if not isfile(DATABASE):
        with open(DATABASE, 'a') as f:
            init()

    """Operations:
    - start: start flaskgur server.
    - newkey: generate new API key.
    - restart: destroys all file references in database.
    """
    if len(argv) == 1:
        app.run(debug=DEBUG, host='0.0.0.0')
    elif len(argv) == 2:
        if argv[1].lower() == "start":
            app.run(debug=DEBUG, host='0.0.0.0')
        elif argv[1].lower() == "newkey":
            print("Your secret API key is: " + addApiKey())
        elif argv[1] == "restart":
            if raw_input("Are you ABSOLUTELY sure? All files will be " +
                         "destroyed! Type 'yes' if you understand. ") == "yes":
                init()
                print("Restarted! Old files have not been purged.")
            else:
                print("Nothing was changed.")
