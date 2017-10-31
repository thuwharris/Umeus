from . import app, db, bcrypt
from .forms import CommentDeleteForm
from flask_bcrypt import generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime as dt
import bbcode
import json
from .config import COMMENTS_PER_PAGE


class User(db.Model):
	"""Model for a user. Includes methods required for flask-login intergration."""

	__tablename__ = 'user'

	user_id       = db.Column(db.Integer, primary_key=True) # Unique identifier for the user
	username      = db.Column(db.String, unique=True)		# Username (must be unique)
	email         = db.Column(db.String, unique=True)		# Email (must be unique)
	_password 	  = db.Column(db.String)					# The hashed password string
	authenticated = db.Column(db.Boolean, default=False)	# Has this account's email
															#   address been authenicated?

	@hybrid_property
	def password(self):
		"""
		Returns the hashed password
		This is a hybrid property, which allows us to implement a setter for
		password, which is _set_password()
		"""
		return self._password

	@password.setter
	def _set_password(self, pw):
		"""Setter for password. Hashes the password with bcrypt before storing"""
		self._password = bcrypt.generate_password_hash(pw)

	def check_password(self, pw):
		return bcrypt.check_password_hash(self._password, pw)

	def is_active(self):
		return True

	def get_id(self):
		return self.user_id

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False

	def get_comments(self):
		"""Get all the comments posted by this user, ordered newest-latest"""
		return BlogComment.query.filter_by(user_id=self.user_id).order_by(BlogComment.datetime.desc()).all()

	@staticmethod
	def username_exists(username):
		"""Checks whether a user exists with this username"""
		return User.query.filter_by(username=username).count() > 0

	@staticmethod
	def email_exists(email):
		"""Checks whether a user exists with this email"""
		return User.query.filter_by(email=email).count() > 0


class BlogPost(db.Model):
	"""Model for a blog post"""
	post_id  = db.Column(db.Integer, primary_key=True)	# Unique identifier for a post
	datetime = db.Column(db.DateTime) # Timestamp of the post
	author	 = db.Column(db.String)   # Name of the author
	title	 = db.Column(db.String)   # Title of the post
	post 	 = db.Column(db.String)	  # Post contents. May contain BBCode
	tags	 = db.Column(db.String)	  # A list of tags seperated by a vertical bar
									  # eg |tag1|tag2|tag3|tag4|
									  # Having a bar at the start and end makes the Regex much simpler

	def render_post(self):
		"""Return the rendered html from the post's bbcode"""
		return bbcode.render_html(self.post)

	def get_sample(self):
		"""Return first 100 characters of the text"""

		# TODO
		# Replace this with a description field!

		return self.post[:100] + '...'

	def get_date(self):
		"""Return a formatted string for the post's timestamp"""
		return self.datetime.strftime('%d %B %Y')

	def get_comments(self):
		"""Return all of the comments on the post, ordered newest-oldest"""
		return BlogComment.query.filter_by(post_id=self.post_id).order_by(BlogComment.datetime.desc()).all()

	def get_page(self, page_num):
		return BlogComment.query.filter_by(post_id=self.post_id).order_by(BlogComment.datetime.desc()).paginate(page_num, COMMENTS_PER_PAGE, False).items

	def comment_count(self):
		"""Returns the number of comments on this post"""
		return BlogComment.query.filter_by(post_id=self.post_id).count()

	def get_tags(self):
		"""Returns an array of the tags on a post"""
		return self.tags.split('|')[1:-1] # Remove the first and last, as they are blank

class BlogComment(db.Model):
	"""Model for a blog comment"""
	comment_id = db.Column(db.Integer, primary_key=True) # Unique identifier for the comment
	user_id    = db.Column(db.Integer, db.ForeignKey(User.user_id)) 	# ID of the author (User)
	post_id	   = db.Column(db.Integer, db.ForeignKey(BlogPost.post_id)) # ID of the post (BlogPost)
	datetime   = db.Column(db.DateTime) # Timestamp of when the comment was posted
	comment    = db.Column(db.String)	# Content of the comment

	user = db.relationship('User', foreign_keys='BlogComment.user_id') 	   # The User object associated with the comment
	post = db.relationship('BlogPost', foreign_keys='BlogComment.post_id') # The BlogComment object associated with the comment

	def render_comment(self):
		"""Return the rendered comment's from the post's bbcode"""
		return bbcode.render_html(self.comment)

	def get_date(self):
		"""Return a formatted string for the comment's timestamp"""
		dt = self.datetime.strftime('%I:%M %p - %d %b %y')
		
		# This is a bit hacky because %-H doesn't work on Heroku
		# If the hour starts with a 0, get rid of it
		# Eg 01:02 -> 1:02
		
		if dt[0] == '0':  
			return dt[1:]
		return dt

	def to_dict(self):
		"""Convert the comment to a dict, for use in JSON"""
		return {
			'username': self.user.username,
			'user_id' :	self.user.user_id,
			'id'	  :	self.comment_id,
			'datetime':	self.get_date(),
			'comment' :	self.render_comment()
		}


def latest_post():
	"""Get the most recently posted post"""
	return BlogPost.query.order_by(BlogPost.datetime.desc()).first()