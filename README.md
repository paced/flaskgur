# flaskgur

Simple image hosting site written with Flask and Python. Forked from chokepoint's flask app, this is an even lighter version that hashes filenames differently and provides a simpler image upload feature. It is meant for use by apps like ShareX or using tools like `maim` and `slop` using POST requests.

## Requirements

The following are hard requirements:

- Python 2.x
- python-pip
- Flask

Optionally, depending on your method of deployment:

- virtualenv
- uwsgi

## Installation

You will of course need to deploy the server yourself, but to just run the server as a test:

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

After this, you may want to play around with the source file. This will allow you to make changes, most obviously to change the extensions allowed.
