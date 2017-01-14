# pipette

Pipette is a self-hosted image and file host that is light, simple, and customisable.

## Features

-   Dead simple operation, accepting POST requests to a URL for file upload.
-   Uses the lightweight Flask Python framework.
-   Shows diagnostics for the entire image database.
-   Core code is extremely easy to understand and adapt.

## Requirements

-   Python 2.x
-   python-pip

We recommend using virtualenv to not clutter your machine's Python installation, but it is not required.

## Installation

```sh
$ git clone https://github.com/paced/pipette && cd pipette
$ pip install -r requirements.txt
$ python pipette.py newkey
$ python pipette.py runserver
```

This will run a test server on localhost:5000 and give you an APIkey in the (default) api.keys file. We recommend using nginx with passenger to host the app.

## Configuration

All configuration settings can be found in settings.py.

## Usage

Send a file by POST request. The arguments are "file" and "apikey". You return a URL to your uploaded file once your upload is finished and processed.

## Extra

-   **Note:** No uploaded file has an expiry date. This is intentional, since this is a private, self-hosted upload service.

-   **Note:** Other people will not be able to upload without an API key. This is intentional, as it will appear as if you, the user, are uploading and sending other people's files.

-   **Note:** File deletion is not possible. I don't believe this is necessary, but a pull request may change my mind.

-   **Warning:** The diagnostics tab does not tell you how much space is remaining on your host's storage. Be careful not to exceed the limit of your host or the app, and your entire server, will break.

## Credits and License

-   Developed and designed by Thomas (Tianhao) Wang.
-   This project is a completely reworked fork of chokepoint's flaskgur app.
-   Favicon/logo design by Hannah Yen.

This project is licensed under GPLv2.0.
