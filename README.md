# pipette

Simple image hosting site written with Flask and Python. Forked from chokepoint's "flaskgur" app (see link below project header), this is an even lighter version that hashes filenames differently and provides a simpler image upload feature. It's meant for use by apps like ShareX or using tools like `maim` and `slop` using POST requests.

As it is now an entirely different app to upstream, I have renamed it to "pipette."

## Differences to sources

As required by GPLv2, I must list the list of changes to the original work:

-   Completely revamped code style and structure.
-   Implemented rate limiting.
-   Implemented compression.
-   Does not use Flask's g(lobal) to manipulate sqlite3 database.
-   Added significant new code
-   Added diagnostics page.
-   Added styling and more basic upload page.
-   Upload page is completely novel.
-   Removed a great deal of code relating to the "gallery."
-   Updated for latest version of flask.

...and other changes outlined by commit messages and history.

## Requirements

The following are hard requirements:

-   Python 2.x
-   python-pip
-   virtualenv

Install the requirements in requirements.txt, as shown here:

-   Flask >= 0.12
-   Flask-HTMLmin >= 1.2
-   Flask-Compressor >= 0.2.0
-   Flask-Limiter >= 0.9.3
-   uwsgi >= 2.0.14
-   cssmin >= 0.2.0
-   jsmin >= 2.2.1

## Installation

You will of course need to deploy the server yourself, but to run the server as a test:

```sh
$ git clone https://github.com/paced/pipette
$ cd pipette
$ python pipette.py newkey
$ cat api.keys
$ python pipette.py
```

This will generate an apikey for you, and start the server on 0.0.0.0:5000. After this, you can send a file to your image host by POST request. The arguments are "file" and "apikey".

After this you may want to look inside the pipette.py file to modify settings. Production servers will immediately want to turn DEBUG to False.

## Todo

-   Add favicon, meta information for main page.
