"""WSGI module."""
from pipette import app as application

if __name__ == "__main__":
    app.run(debug=pipette.DEBUG, host='0.0.0.0')
