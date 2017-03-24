<p align="center">
<img src=imagehost/static/images/pipette.png alt="Pipette!" />
</p>

# pipette

Pipette is a self-hosted image and file host that is light, simple, and customisable. See an example of the web frontend [here](https://i.paced.me).

## Features

-   Dead simple operation, accepting POST requests to a URL for file upload.
-   Uses the lightweight Flask Python framework.
-   Works with both Python 2.x and 3.x.
-   Shows diagnostics for the entire image database.
-   Core code is extremely easy to understand and adapt.

## Requirements

-   Python
-   python-pip

We recommend using virtualenv to not clutter your machine's Python installation, but it is not required.

## Installation

```sh
$ git clone https://github.com/paced/pipette && cd pipette
$ pip install -r requirements.txt && cd imagehost
$ python pipette.py newkey
$ python pipette.py runserver
```

That's it, you're live! But you'll probably want an API key:

```sh
$ cat api.keys
```

After that, you'll want some way to keep Python running forever. I suggest using Passenger with NginX for this, but do whatever suits you.

## Configuration

All configuration settings can be found in settings.yaml. One of these configurations is for deleting files after removing URLs from the database. By default, files are stashed and not deleted after being moved to the /pics/stash folder, and this folder is not included in /diagnostic's size calculation. We have included a script to run a cron job to periodically delete the backups in the /pics/stash folder, but you must schedule it yourself. First, you might want to edit the file as it makes assumptions about where you're running it from:

```sh
$ vim autodelstash.sh  # Found in repo root directory.
```

Then, edit your scheduled cron jobs:

```sh
$ crontab -e
```

Then, at the bottom, write something like this:

```sh
30 8 * * * bash /path/to/pipette/imagehost/autodelstash.sh > /dev/null 2>&1
```

Use at your own risk. If you don't know how this works, I suggest either deleting them manually, deleting them automatically, or not deleting them at all.

## Usage

Send a file by POST request with a file: "file" and field "apikey". The HTTP response is a URL, or a failure code. ShareX and curl are great tools to use this with.

Delete a file by POST request to /delete/<file>. Include field "apikey" and the file will be immediately deleted without confirmation. Be careful!

## Credits and License

-   Developed and designed by Thomas (Tianhao) Wang.
-   This project is a completely reworked fork of chokepoint's flaskgur app.
-   Favicon/logo design by Hannah Yen.

This project is licensed under GPLv2.0.

## Changelog

-   15th January 2017
    -   Project completed, first release 1.0.0 packaged.
-   24th March 2017
    -   File deletion is now possible.
    -   We're now using YAML for settings rather than creating a settings.py file.
    -   Tested on Python 3.6.
    -   Lots of style changes.
