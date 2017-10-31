from .. import app, db
from flask import render_template, redirect, url_for, abort, request, jsonify
from flask_login import current_user
from datetime import datetime
import json

from ..util import json_error
from ..config import COMMENTS_PER_PAGE

# Forms
from ..forms import CommentForm, CommentDeleteForm

# Models
from ..models import User, BlogPost, BlogComment, latest_post


@app.route('/blog/')
def blog():
	# Redirect to the most recent post
	return redirect(url_for('blog_post', post_id=latest_post().post_id))

@app.route('/blog/<int:post_id>/', methods=['GET','POST'])
def blog_post(post_id):
	"""
	View a blog post with BlogPost.post_id=post_id
	Isn't cached because the comment submission requires a fresh CSRF token and ReCAPTCHA
	This might need to be changed depending on performance
	"""

	#Create a form object for the comment form
	com_form = CommentForm()

	if com_form.validate_on_submit():
		#If the form has been submitted, create a new BlogComment and commit
		comment = BlogComment(
				post_id = post_id,
				user_id = current_user.user_id,
				comment = com_form.comment.data,
				datetime = datetime.now()
			)
		db.session.add(comment)

		try:
			db.session.commit()
		except Exception as e:
			print(e)

	# Create an object for the comment deletion form
	del_form = CommentDeleteForm()

	# Get the post with this ID
	post = BlogPost.query.filter_by(post_id=post_id).first_or_404()
	# Render the contents
	postcont = post.render_post()
	# Get the list of tags
	tags = post.get_tags()

	# Get a list of posts to display in the sidebar
	sidebar = BlogPost.query.order_by(BlogPost.datetime.desc()).all()

	# Get a list of comments
	comments = post.get_comments()

	return render_template('blog/blog.html', post_id=post.post_id, title=post.title,
					author=post.author, date=post.get_date(), post=postcont, tags=tags,
					sidebar=sidebar, comments=comments, com_form=com_form, del_form=del_form)

@app.route('/blog/get_comments/', methods=['GET'])
def get_comments():
	"""
	Returns a JSON object containing the comments on a particular page

	GET ARGUMENTS:
		post_id:  The ID of the blog post
		page_num: The page number (counting starts at 1)

	JSON RESULT:
		post_id:	   	The ID of the blog post
		page_num:		The page number (counting starts at 1)
		com_per_page:	The number of comments per page (config.COMMENTS_PER_PAGE)
		comment_count: 	The total number of comments on the post
		comments:	   	An array of the comments (see models.BlogComment.serialise)	

	ERROR RESULT:
		Returns a JSON object containing a status code and a message giving more detail
	"""

	if ('post_id' in request.args) and ('page_num' in request.args):
		try:
			post_id = int(request.args['post_id'])
			page_num = int(request.args['page_num'])
			identifier = 'post_id.%d.%d' % (post_id, page_num)

			post = BlogPost.query.get(post_id)
			com_count = post.comment_count()

			# Returns [] if there the page number is too big
			# Returns the first page is the page number <= 0
			com = post.get_page(page_num)
			
			if com == []:
				if page_num == 1:
					return json_error(status=400, message='This post has no comments')
				return json_error(status=400, message='Invalid page number')
			
			return jsonify({
				'post_id'		: post_id,
				'page_num'		: page_num,
				'com_per_page'	: COMMENTS_PER_PAGE,
				'comment_count' : com_count,
				'comments'		: [c.to_dict() for c in com]
			})

		except Exception as ex:
			# This is called in 2 circumstances:
			# 	- post_id or page_num arguments cannot be cast to ints
			#	- There isn't a BlogPost object with the input post ID
			return json_error(status=400, message='Invalid query - post number or page number not valid')

	return json_error(status=400, message='Invalid query - missing arguments')

@app.route('/blog/delete_comment/', methods=['POST'])
def delete_comment():
	form = CommentDeleteForm()

	# If a form has been submitted
	if form.validate_on_submit():
		# Get the BlogComment object with this ID
		# If there isn't one, abort with a 404 error
		comment = BlogComment.query.filter_by(comment_id=form.comment_id.data).first_or_404()

		#Store the ID of the post for later use
		post_id = comment.post_id

		# Check that the current user is the one who posted the comment
		if comment.user_id == current_user.user_id:
			# Delete the comment, and commit
			db.session.delete(comment)
			db.session.commit()
			# Redirect to the original blog post
			return redirect(url_for('blog_post', post_id=post_id))


	return abort(403)

@app.route('/blog/tagged/<tag>')
def blog_tagged(tag):

	query = '%|' + tag + '|%'
	posts =   BlogPost.query.filter(BlogPost.tags.like(query)).order_by(BlogPost.datetime.desc()).all()
	sidebar = BlogPost.query.order_by(BlogPost.datetime.desc()).all()

	if not posts:
		return render_template('blog/tagged_fail.html', tag=tag, sidebar=sidebar)

	return render_template('blog/tagged.html', tag=tag, posts=posts, sidebar=sidebar)
