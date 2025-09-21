$(document).ready(function () {
	const form = $('#register-form');
	let msgBox = $('#response-message');
	if (msgBox.length === 0) {
		msgBox = $('<div id="response-message"></div>').css({
			'margin-top': '1rem',
			'text-align': 'center',
			'font-size': '1rem',
			'border-radius': '0.5rem',
			'padding': '0.7rem 0.5rem',
			'display': 'none'
		});
		form.after(msgBox);
	}

	function showMessage(type, text) {
		msgBox.text(text)
			.css('color', type === 'success' ? '#4ee34e' : '#ff4e4e')
			.css('background', type === 'success' ? '#1e2e1e' : '#2e1e1e')
			.fadeIn(200);
	}

	function validateUsername(username) {
		return /^[A-Za-z0-9_]{3,32}$/.test(username);
	}

	function validatePassword(password) {
		return password.length >= 6 && !/\s/.test(password);
	}

	function validateToken(token) {
		return token.length >= 10 && !/\s/.test(token);
	}

	form.on('submit', function (e) {
		e.preventDefault();
		msgBox.hide();

		const username = $('#username').val().trim();
		const password = $('#password').val();
		const token = $('#token').val().trim();

		if (!validateUsername(username)) {
			showMessage('error', 'Username can only contain letters, numbers, and underscores, with no spaces.');
			return;
		}
		if (!validatePassword(password)) {
			showMessage('error', 'Password must be at least 6 characters and contain no spaces.');
			return;
		}
		if (!validateToken(token)) {
			showMessage('error', 'Token must be at least 10 characters and contain no spaces.');
			return;
		}

		$.ajax({
			url: '/api/register',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({ username, password, token }),
			success: function (resp) {
				if (resp.success) {
					showMessage('success', resp.success);
					form[0].reset();
				} else if (resp.error) {
					showMessage('error', resp.error);
				} else {
					showMessage('error', 'Unexpected server response.');
				}
			},
			error: function (xhr) {
				let msg = 'Connection error with the server.';
				if (xhr.responseJSON && xhr.responseJSON.error) {
					msg = xhr.responseJSON.error;
				}
				showMessage('error', msg);
			}
		});
	});
});
