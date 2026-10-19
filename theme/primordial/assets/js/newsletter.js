/* Newsletter signup: posts to Kit's public form endpoint and shows the result in place. */
(function () {
	var SUCCESS = 'Almost there — check your inbox (and Promotions/Spam) and click the link to confirm.';
	var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

	document.querySelectorAll('[data-pp-news]').forEach(function (form) {
		var input = form.querySelector('input[name="email_address"]');
		var button = form.querySelector('button[type="submit"]');
		var status = form.querySelector('.pp-news-status');

		function say(msg, kind) {
			status.textContent = msg;
			status.className = 'pp-news-status' + (kind ? ' is-' + kind : '');
		}

		form.addEventListener('submit', function (e) {
			e.preventDefault();
			var email = (input.value || '').trim();
			if (!EMAIL.test(email)) {
				say('Please enter a valid email address.', 'error');
				input.focus();
				return;
			}
			button.disabled = true;
			say('Sending…');

			var data = new FormData();
			data.append('email_address', email);

			fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' }, credentials: 'omit' })
				.then(function (r) { return r.json().catch(function () { return { status: r.ok ? 'success' : 'error' }; }); })
				.then(function (j) {
					if (j && (j.status === 'success' || j.status === 'quarantined')) {
						form.classList.add('is-done');
						say(SUCCESS, 'ok');
					} else {
						var msg = (j && j.errors && j.errors.messages && j.errors.messages[0]) || 'Something went wrong. Please try again.';
						say(msg, 'error');
						button.disabled = false;
					}
				})
				.catch(function () {
					// If the browser blocks the background request, fall back to a normal form post.
					form.removeAttribute('data-pp-news');
					HTMLFormElement.prototype.submit.call(form);
				});
		});
	});
})();
