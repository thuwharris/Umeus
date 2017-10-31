from itsdangerous import URLSafeTimedSerializer
from flask import jsonify
from . import app

ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def json_error(status=404, message='Something went wrong'):
	"""
	Returns a standardised error message in JSON
	err_status  : The status of the error (404 by default)
	err_message : The specific error message
	"""
	json = {
		'err_status' : status,
		'err_message': message
	}
	resp = jsonify(json)
	resp.status_code = status
	return resp