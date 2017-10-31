
$(document).ready(function() {
	setTimeout('validateForm()', 2000);
});


function validateEmail() {
	var email = $('#email');
	//TODO validate properly.

	email.removeClass('has-warning');
	email.addClass('form-control-success');
}

function validateForm() {
	var email = $('#email').val();
	var username = $('#username').val();
	
	if(email != '')
		validateEmail();

}

function submitForm() {

}