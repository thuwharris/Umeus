from .. import app, cache
from flask import render_template

@app.route('/intdev/')
def intdev_index():
	"""
	Index page for the international development section
	"""
	return render_template('intdev/index.html')