from .. import app, db, cache
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from ..forms import LoginForm, SignupForm, ContactForm
from ..models import User

@app.route('/')
def index():
	"""The homepage of the website"""
	return render_template('main/index.html')

@app.route('/account/')
@login_required
def account():
	# TODO
	# Will be implemented later
	pass

@app.route('/login/', methods=['GET','POST'])
def login():
	"""
	The page containing the login form
	This page should not be cached, as the CSRF and Recaptcha should be different each visit
	"""

	form = LoginForm()

	# If data was sent in the form
	if form.validate_on_submit():

		# Lowercase username
		username = form.username.data.lower()

		if not User.username_exists(username):
			return render_template('main/login.html',form=form, error='Username does not exist')

		# Find the username
		user = User.query.filter_by(username=form.username.data).first()

		# Check the password
		if user.check_password(form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('index'))
		else:
			return render_template('main/login.html', form=form, error='Incorrect password!')

	return render_template('main/login.html', form=form)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	"""
	The page containing the signup form
	This page should not be cached, as the CSRF and Recaptcha should be different each visit
	"""

	form = SignupForm()

	# If data was sent in the form
	if form.validate_on_submit():

		# Lowercase usernames and emails
		username = form.username.data.lower()
		email = form.email.data.lower()

		# Does the username exist?
		if User.username_exists(username):
			return render_template('main/signup.html', form=form, error='This username has already been taken')

		# Does the email exist?
		if User.email_exists(email):
			return render_template('main/signup.html', form=form, error='This email is already in use')

		# Create the user and add them
		user = User(
			username = username,
			email 	 = email,
			password = form.password.data,
			authenticated = True # Remove when email confirmation is implemented
		)
		db.session.add(user)
		db.session.commit()


		# TODO
		# Implement email confirmation
		'''
		subject = 'Confirm your email'
		token = ts.dumps(self.email, salt='email-confirm-key')

		confirm_url = url_for('confirm_email', token=token, _external=True)
		html = render_template('emails/confirm.html', confirm_url=confirm_url)

		send_email(user.email, subject, html)
		'''

		return redirect(url_for('login'))

	return render_template('main/signup.html', form=form)

@app.route('/logout/')
@login_required
def logout():
	"""Logout the user using Flask-Login"""
	logout_user()
	return redirect(url_for('index'))


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
	"""
	The page containing the 'contact us' form
	This page should not be cached, as the CSRF and Recaptcha should be different each visit
	"""
	form = ContactForm()

	if form.validate_on_submit():
		#SEND THE FORM
		return render_template('main/contact.html', form=form, success=True, email='', message='')

	# If there is data in the form and the form didn't send, put the
	# submitted values back into the inputs.
	email = form.email.data or ''
	message = form.message.data or ''

	return render_template('main/contact.html', form=form, success=False, email=email, message=message)

@app.route('/about/')
def about():
	"""Static about page, cached as 'about'"""
	return render_template('main/about.html')

@app.route('/privacy/')
def privacy():
	"""Static privacy page, cached as 'privacy'"""
	return render_template('main/privacy.html')

@app.route('/legal/')
def legal():
	"""Static legal page, cached as 'legal'"""
	return render_template('main/legal.html')
