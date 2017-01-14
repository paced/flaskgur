# pipette

Pipette is a self-hosted image and file host that is light, simple, and customisable. Anybody with a web host can use it

## Features

-   Dead simple operation, accepting POST requests only for file upload.
-   Uses the lightweight Flask Python framework.
-   Shows diagnostics for the entire image database.

## Requirements

-   Python 2.x
-   python-pip
-   virtualenv

## Installation

```sh
$ git clone https://github.com/paced/pipette
$ cd pipette
$ pip install -r requirements.txt
$ python pipette.py newkey
$ cat api.keys
```

Copy and save the API key provided to you. To upload a file, you will need one of these API keys. After this, you should edit settings.py and run a test server on localhost:5000 by doing:

```sh
$ python pipette.py
```

## Usage

Send a file by POST request. The arguments are "file" and "apikey".

## Warnings

The diagnostics tab does not tell you how much space is remaining on your host's storage. Be careful not to exceed the limit of your host or the app, and your entire server, will break.

## Todo

-   Add favicon, change logo.
-   Change into a pip module by allowing user to import, set own settings, and make APIkey creation a module function.
