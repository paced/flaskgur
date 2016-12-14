from flask import Flask, request, g, redirect, url_for, abort, render_template, send_from_directory
from werkzeug import secure_filename
from hashlib import md5
import Image
import sqlite3
import os
import time

DEBUG              = True
UPLOAD_DIR         = 'pics'
DATABASE           = 'flaskgur.db'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webm', 'mp4'])

app = Flask(__name__)
app.config.from_object(__name__)

# Make sure extension is in the ALLOWD_EXTENSIONS set
def check_extension(extension):
	return extension in ALLOWED_EXTENSIONS

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# Insert filename into database	
def add_pic(filename):
	g.db.execute('insert into pics (filename) values (?)', [filename])
	g.db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET','POST'])
def upload_pic():
	if request.method == 'POST':
		file = request.files['file']
		try:
			extension = file.filename.rsplit('.', 1)[1].lower()
		except IndexError, e:
			abort(404)
		if file and check_extension(extension):
			# Salt and hash the file contents
			filename = md5(file.read() + str(round(time.time() * 1000))).hexdigest() + '.' + extension
			file.seek(0) # Move cursor back to beginning so we can write to disk
			file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
			add_pic(filename)
			gen_thumbnail(filename)
			return redirect(url_for('show_pic', filename=filename))
		else: # Bad file extension
			abort(404)
	else:
		return render_template('upload.html', pics=get_last_pics())

@app.route('/<filename>')
def return_pic(filename):
	return send_from_directory(app.config['UPLOAD_DIR'], secure_filename(filename))
	
if __name__ == '__main__':
	app.run(debug=DEBUG, host='0.0.0.0')
