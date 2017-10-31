
// Load a page of comments.
// Will hide the correct page, show the loading gif,
// run the AJAX call, load the page and load the pagination list.
// Also handles any errors that may occur.
function loadCommentPage(pageNumber) {

	$('#loading').show(); // Show the loading gif
	$('#comment_list').empty(); // Hide the comment list
	$('#pagination').hide(); // Hide the pagination list

	// Make the AJAX call to /blog/get_comments
	$.ajax({
		url: '/blog/get_comments',
		type: 'GET',
		dataType: 'json',

		data: {
		  post_id: postID,
		  page_num: pageNumber
		}
	})
	.done(function(json) {
		// When the AJAX succeeds, get the page number from the returned json
  		pageNum = json.page_num;

  		// Load the page of comments
		loadComments(json.comments);

		// Load the pagination list
		loadPagination(json.page_num, json.comment_count, json.com_per_page);
	})
	.fail(function(xhr,status,errorThrown) {
		// If the AJAX fails, get the returned json
		var json = xhr.responseJSON;

		// If a response is given, and the response's message is that a post has no comments
		if(json && json.err_message == 'This post has no comments') {
		  $('#error').text('This post has no comments').show();
		} else {
		  $('#error').html('Something went wrong...<br/>Please reload the page').show();
		}

		pageNum = -1;
		console.log(xhr.responseJSON.err_status);
		console.log(xhr.responseJSON.err_message);
	})
	.always(function() {
		// Always hide the loading GIF when the AJAX has finished
		$('#loading').hide();
	});
}

// Load a page of comments into the list
function loadComments(comments) {
	for(var i = 0; i<comments.length; i++) {

		var c = comments[i];
		
		// Container div for the comment
		var com = $('<div>', {class:'list-group-item'});

		// Div for the heading (contains name, date, delete button)
		var heading = $('<div>', {class:'list-group-item-heading', style:'height:40px'});
		var nameDate = $('<div>', {class:'col-md-8'});
		
		// Add the username and the date to the heading
		nameDate.append(
		  $('<h4>').html(
			c.username + '  <small class="text-muted"><i>' + c.datetime + '</i></small>'
		  )
		);
		heading.append(nameDate);

		// If the comment is written by the current user, show the delete button
		// Correct user ID is also checked serverside
		if(c.user_id == userID) {
		  var delDiv = $('<div>', {id:'comDel'+c.id, class:'col-md-4'});
		  var button = $('<input>', {
				type:'submit',
				class: 'btn btn-warning pull-right',
				value: 'Delete Comment',
				onclick: 'javascript:comDel('+c.id+')'
		  });
		  delDiv.append(button);
		  heading.append(delDiv);
		}

		com.append(heading);

		// Create the div containing the comment's content
		var contDiv = $('<div>', {class:'clearfix'});
		var contP = $('<p>', {class:'list-group-item-text'}).html(c.comment);
		contDiv.append(contP);
		com.append(contDiv);

		// Add the comment to the list
		$('#comment_list').append(com);
	}
}

// Create the pagination list.
// (the page numbers)
function loadPagination(pageNum, commentCount, comPerPage) {

	// Calculate the number of pages
	var numPages = Math.ceil(commentCount / comPerPage);

	var prevButton = $('#pagination-prev');
	var nextButton = $('#pagination-next');

	// If this is the first page, previous should be disabled	
	if(pageNum == 1)
		prevButton.addClass('disabled');
	else
		prevButton.removeClass('disabled');

	// If this is the last page, next should be disabled
	if(pageNum == numPages)
		nextButton.addClass('disabled');
	else
		nextButton.removeClass('disabled');

	// Remove all of the page numbers on the list
	$('.page-num').remove();

	// Elements need to start being added after the previous button
	var elemToBeAppended = prevButton;

	for(var i = 1; i <= numPages; i++) {
		var item = mkPaginationItem(i, (i==pageNum), true);

		elemToBeAppended.after(item);
		elemToBeAppended = item;
	}

	$('#pagination').show();
}

// Create a <li> element for a page number
// i - the number of the page
// active - Is this the current page
// enabled - Is the item 
function mkPaginationItem(i, active, enabled) {

	var id = 'pagination-' + i;

	// Create the content of the item
	var cont = $('<a>', { class: 'page-link', href: 'javascript:loadCommentPage('+i+')' })
				 .text(i); // Set the text to the page number

	var item = $("<li>", { class: 'page-item page-num', id: id}).append(cont);

	if(active)
		item.addClass('active');
	if(!enabled)
		item.addClass('disabled');

	return item;
}

function nextPage() {
	loadCommentPage(pageNum + 1);
}

function prevPage() {
	loadCommentPage(pageNum - 1);
}

function comDel(id) {
	$('#comment_id').val(id);
	$('#deleteConfirmModal').modal();
}