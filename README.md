# flaskgur

Simple image hosting site written with Flask and Python. Forked from chokepoint's flask app, this is an even lighter version that hashes filenames differently and provides a simpler image upload feature. It's meant for use by apps like ShareX or using tools like `maim` and `slop` using POST requests.

## Requirements

The following are hard requirements:

-   Python 2.x
-   python-pip
-   Flask >= 0.12
-   Flask-HTMLmin

Optionally, depending on your method of deployment:

-   virtualenv
-   uwsgi

## Installation

You will of course need to deploy the server yourself, but to run the server as a test:

```sh
$ git clone https://github.com/paced/flaskgur
$ cd flaskgur
```

You will have to edit the SERVER global var to your domain or IP address, then:

```sh
$ python flaskgur.py newkey
$ cat api.keys
$ python flaskgur.py
```

This will generate an apikey for you, and start the server on 0.0.0.0:5000. After this, you can send a file to your image host by POST request. The arguments are "file" and "apikey".

After this, you may want to play around with the source file. This will allow you to make changes, most notably to change the extensions allowed.

## Todo

-   Add favicon, meta information for main page.
-   Remove any and all exif (metainfo) from photos after upload.
-   Simple admin monitoring of resource usage, all ID's used, the number of ID's left for each file type.
-   OSX has poor substitutes to ShareX. Image uploading is easy, but not file uploads (mp3, .txt, .py, .c, etc), and video uploads. I think I'll create a FOSS script or program (cross-platform) that allows custom upload sources, error handling, screen region recording (both video and image), file upload in context menu, and progress meter.
