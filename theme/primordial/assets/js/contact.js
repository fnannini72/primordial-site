/* Contact form: fetches a signed token on first interaction, then sends via the REST API. */
(function () {
	var form = document.querySelector('[data-pp-contact]');
	if (!form || !window.ppContact) return;

	var status = form.querySelector('.pp-form-status');
	var button = form.querySelector('button[type="submit"]');
	var topic = form.querySelector('#pp-topic');
	var token = null;
	var tokenPromise = null;

	// Preselect a topic from the URL: /contact/?topic=coaching
	var wanted = new URLSearchParams(location.search).get('topic');
	if (wanted && topic.querySelector('option[value="' + wanted.replace(/[^a-z-]/g, '') + '"]')) {
		topic.value = wanted;
	}

	function getToken() {
		if (!tokenPromise) {
			tokenPromise = fetch(ppContact.token, { cache: 'no-store', credentials: 'omit' })
				.then(function (r) { return r.json(); })
				.then(function (j) { token = j.t; return token; })
				.catch(function () { tokenPromise = null; return null; });
		}
		return tokenPromise;
	}
	form.addEventListener('focusin', getToken, { once: true });
	form.addEventListener('pointerdown', getToken, { once: true });

	function say(msg, kind) {
		status.textContent = msg;
		status.className = 'pp-form-status' + (kind ? ' is-' + kind : '');
	}

	form.addEventListener('submit', function (e) {
		e.preventDefault();
		var data = Object.fromEntries(new FormData(form).entries());
		if (!data.name || !data.email || !data.topic || !data.message) {
			say('Please fill in name, email, topic and message.', 'error');
			return;
		}
		button.disabled = true;
		say('Sending…');
		getToken().then(function (t) {
			data.t = t || '';
			return fetch(ppContact.send, {
				method: 'POST',
				credentials: 'omit',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(data)
			});
		}).then(function (r) { return r.json(); }).then(function (j) {
			if (j && j.ok) {
				form.reset();
				form.classList.add('is-sent');
				say('Thank you. Your message is on its way, and you will hear back soon.', 'ok');
			} else {
				say((j && j.message) || 'Sorry, something went wrong. Please try again.', 'error');
				button.disabled = false;
				if (j && /reload/.test(j.message || '')) { tokenPromise = null; }
			}
		}).catch(function () {
			say('Connection problem. Please try again in a moment.', 'error');
			button.disabled = false;
		});
	});
})();
