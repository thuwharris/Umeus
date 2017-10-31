from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required

class LoginForm(Form):
	"""Form used on the login page"""

	username  = StringField('username',   validators=[DataRequired(message='Username field cannot be empty')])
	password  = PasswordField('password', validators=[DataRequired(message='Password field cannot be empty')])
	remember  = BooleanField('remember')


class SignupForm(Form):
	"""Form used on the signup page"""
	username  = StringField('username', validators=[DataRequired(message='Username field cannot be empty'),
												    Length(min=5, max=32, message='Username must be between 5 and 32 characters')])
	
	email 	  = StringField('email', validators=[DataRequired(message='Email field cannot be empty'),
												 Email(message='Not a valid email address')])

	password  = PasswordField('password', validators=[DataRequired(message='Password field cannot be empty'),
													  EqualTo('confirm', message='Passwords must match')])

	confirm	  = PasswordField('confirm', validators=[DataRequired(message='Confirmation field cannot be empty')])
	tos		  = BooleanField('tos', validators=[Required(message='You must accept the terms of service')])
	recaptcha = RecaptchaField()


class ResetForm(Form):
	"""Form used for password resets"""
	email 	  = StringField('email', validators=[DataRequired(message='Email field cannot be empty'),
											     Email(message='Not a valid email address')])
	recaptcha = RecaptchaField()


class ContactForm(Form):
	"""Form used on the contact us page"""
	email 	  = StringField('email',   validators=[DataRequired(message='Email field cannot be empty'),
												   Email(message='Not a valid email address')])
	message   = StringField('message', validators=[DataRequired(message='Message field cannot be empty'),
												   Length(min=5, max=1024, message='Message must be between 5 and 1024 characters')])
	recaptcha = RecaptchaField()


class CommentForm(Form):
	"""Form used to post a comment on a blog post"""
	comment   = StringField('comment', validators=[DataRequired(message='Comment field cannot be empty'),
												   Length(min=5, max=512, message='Comment must be between 5 and 512 characters')])
	recaptcha = RecaptchaField()

class CommentDeleteForm(Form):
	"""
	Form used to delete a comment.
	This uses a hidden form on the blog page containing the ID of the comment to be deleted
	This allows us to use WTF's CSRF protection
	"""
	comment_id = IntegerField('comment_id', validators=[DataRequired(message='Something went wrong!')])