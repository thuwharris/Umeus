from . import main, blog, intdev
from .. import app
from flask import render_template

#### ERROR MESSAGES ####

@app.errorhandler(404)
def err_404(e):
	return render_template('error/404.html', err=e), 404

@app.errorhandler(500)
def err_500(e):
	return render_template('error/500.html', err=e), 500