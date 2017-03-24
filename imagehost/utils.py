"""Utilities for pipette module."""

import os

ENTROPY = 64


def addApiKey():
    """Add an API key to the api.keys file."""
    with open('api.keys', "a") as f:
        key = hash(ENTROPY)
        f.write(key + '\n')

        return key


def dictSet(d, k):
    """Safely returns the value of a dictionary or returns an empty string."""
    try:
        return d[k]
    except KeyError:
        return ""


def dirExists(path):
    """Ensure a directory exists. If not, creates it."""
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def byteHumanise(num, suffix='B'):
    """Humanise bytes. Code thanks to SO user Sridhar Ratnakumar."""
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Pi', suffix)


def getDirSize(dir):
    """Get the size of a directory (flat)."""
    try:
        s = 0

        for f in os.listdir(dir):
            if os.path.isfile(dir + '/' + f):
                s += os.path.getsize(dir + '/' + f)
    except OSError:
        s = 0

    return byteHumanise(s)
