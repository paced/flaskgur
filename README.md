# pipette

Simple image hosting site written with Flask and Python. Forked from chokepoint's "flaskgur" app (see link below project header), this is an even lighter version that hashes filenames differently and only allows POST upload. It's meant for use by apps like ShareX or using tools like `maim` and `slop` using POST requests.

As it is now an entirely different app to upstream, I have renamed it to "pipette."

## Requirements

-   Python 2.x
-   python-pip
-   virtualenv

## Installation

```sh
$ git clone https://github.com/paced/pipette
$ cd pipette
$ python pipette.py newkey
$ cat api.keys
```

Copy and save the API key provided to you. To upload a file, you will need one of these API keys. After this, you should edit settings.py and run a test server on localhost:5000 by doing:

```sh
$ python pipette.py
```

## Usage

Send a file by POST request. The arguments are "file" and "apikey".

## Todo

-   Add favicon, change logo.
