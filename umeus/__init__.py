from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug.contrib.cache import SimpleCache
from flask.ext.compress import Compress

import bbcode

# Create the app object
app = Flask(__name__)
app.config.from_object('umeus.config')

#Create the database
db = SQLAlchemy(app)

#Create the encryption
bcrypt = Bcrypt(app)

#Create the cache
cache = SimpleCache()

#Enable GZIP compression with Flask-Compress
Compress(app)

#Import views and models
from . import views, models

#Create the login manager
from .models import User
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter(User.user_id==user_id).first()