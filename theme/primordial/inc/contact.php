<?php
/**
 * Contact form: shortcode [pp_contact_form], REST endpoints, message archive.
 *
 * Anti-bot layers (no third-party CAPTCHA, so no extra cookies or consent):
 * 1. The form only works with JavaScript: a signed token is fetched from the server on first interaction.
 * 2. Time trap: the token must be at least a few seconds old and at most two hours.
 * 3. Honeypot field that people never see.
 * 4. Rate limit per IP address.
 * 5. Content checks: too many links or a non-email address are rejected.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const PP_CONTACT_TO        = 'info@primordial-protocol.com';
const PP_CONTACT_MIN_AGE   = 4;            // Seconds between first interaction and send.
const PP_CONTACT_MAX_AGE   = 2 * HOUR_IN_SECONDS;
const PP_CONTACT_RATE      = 5;            // Messages per IP per hour.
const PP_CONTACT_KEEP_DAYS = 730;          // Archive retention (24 months, as in the privacy policy).

function pp_contact_topics() {
	return array(
		'coaching'         => 'One-to-one coaching',
		'survival-courses' => 'Survival courses',
		'retreats'         => 'Retreats & seminars',
		'tailored-events'  => 'Tailored events',
		'team-building'    => 'Team building',
		'psychometric'     => 'Psychometric evaluation',
		'substack'         => 'Substack collaboration',
		'speaking'         => 'Talks, podcasts & interviews',
		'press'            => 'Press & media',
		'other'            => 'Something else',
	);
}

/* ---------- Message archive (private, admin only) ---------- */

add_action( 'init', function () {
	register_post_type( 'pp_message', array(
		'labels'          => array(
			'name'          => 'Messages',
			'singular_name' => 'Message',
			'menu_name'     => 'Messages',
			'all_items'     => 'All messages',
		),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'show_in_rest'    => false,
		'menu_position'   => 25,
		'menu_icon'       => 'dashicons-email-alt',
		'supports'        => array( 'title', 'editor' ),
		'capability_type' => 'post',
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
		'map_meta_cap'    => true,
	) );
} );

// Delete archived messages older than the retention period, once a day.
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'pp_contact_cleanup' ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'pp_contact_cleanup' );
	}
} );
add_action( 'pp_contact_cleanup', function () {
	$old = get_posts( array(
		'post_type'      => 'pp_message',
		'post_status'    => 'any',
		'posts_per_page' => 200,
		'fields'         => 'ids',
		'date_query'     => array( array( 'before' => PP_CONTACT_KEEP_DAYS . ' days ago' ) ),
	) );
	foreach ( $old as $id ) {
		wp_delete_post( $id, true );
	}
} );

/* ---------- REST endpoints ---------- */

function pp_contact_sign( $ts ) {
	return hash_hmac( 'sha256', 'pp-contact|' . $ts, wp_salt( 'nonce' ) );
}

function pp_contact_ip() {
	return isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'pp/v1', '/contact-token', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			nocache_headers();
			$ts = time();
			return array( 't' => $ts . '.' . pp_contact_sign( $ts ) );
		},
	) );

	register_rest_route( 'pp/v1', '/contact', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => 'pp_contact_handle',
	) );
} );

function pp_contact_fail( $msg, $code = 400 ) {
	return new WP_REST_Response( array( 'ok' => false, 'message' => $msg ), $code );
}

function pp_contact_handle( WP_REST_Request $req ) {
	nocache_headers();
	$generic = 'Sorry, the message could not be sent. Please try again in a minute.';

	// 1. Honeypot: silently pretend success so bots learn nothing.
	if ( '' !== trim( (string) $req->get_param( 'website' ) ) ) {
		return array( 'ok' => true );
	}

	// 2. Signed token + time trap.
	$token = (string) $req->get_param( 't' );
	$parts = explode( '.', $token, 2 );
	if ( 2 !== count( $parts ) || ! hash_equals( pp_contact_sign( $parts[0] ), $parts[1] ) ) {
		return pp_contact_fail( $generic );
	}
	$age = time() - (int) $parts[0];
	if ( $age < PP_CONTACT_MIN_AGE ) {
		return pp_contact_fail( 'That was quick! Please wait a few seconds and send again.' );
	}
	if ( $age > PP_CONTACT_MAX_AGE ) {
		return pp_contact_fail( 'This page has been open for a while. Please reload it and send again.' );
	}

	// 3. Rate limit per IP.
	$key   = 'pp_ct_' . md5( pp_contact_ip() );
	$count = (int) get_transient( $key );
	if ( $count >= PP_CONTACT_RATE ) {
		return pp_contact_fail( 'Too many messages from this connection. Please try again later.', 429 );
	}

	// 4. Fields.
	$topics  = pp_contact_topics();
	$name    = sanitize_text_field( (string) $req->get_param( 'name' ) );
	$email   = sanitize_email( (string) $req->get_param( 'email' ) );
	$org     = sanitize_text_field( (string) $req->get_param( 'org' ) );
	$topic   = sanitize_key( (string) $req->get_param( 'topic' ) );
	$message = sanitize_textarea_field( (string) $req->get_param( 'message' ) );

	if ( mb_strlen( $name ) < 2 || mb_strlen( $name ) > 100 ) {
		return pp_contact_fail( 'Please enter your name.' );
	}
	if ( ! is_email( $email ) ) {
		return pp_contact_fail( 'Please enter a valid email address.' );
	}
	if ( ! isset( $topics[ $topic ] ) ) {
		return pp_contact_fail( 'Please choose a topic.' );
	}
	if ( mb_strlen( $message ) < 10 ) {
		return pp_contact_fail( 'Please write a few words about your request.' );
	}
	if ( mb_strlen( $message ) > 5000 || mb_strlen( $org ) > 150 ) {
		return pp_contact_fail( 'The message is too long. Please shorten it a little.' );
	}
	if ( preg_match_all( '#https?://|www\.#i', $message ) > 3 ) {
		return pp_contact_fail( 'Please include no more than three links.' );
	}

	set_transient( $key, $count + 1, HOUR_IN_SECONDS );

	$label = $topics[ $topic ];

	// 5. Archive copy, so nothing is lost if email delivery fails.
	$body = "Topic: {$label}\nName: {$name}\nEmail: {$email}\n" . ( $org ? "Organization: {$org}\n" : '' ) . "\n{$message}";
	$id   = wp_insert_post( array(
		'post_type'    => 'pp_message',
		'post_status'  => 'private',
		'post_title'   => "{$label} — {$name}",
		'post_content' => $body,
	) );

	// 6. Email to the inbox, with Reply-To set to the sender.
	$subject = "[Website] {$label} — {$name}";
	$headers = array(
		'Content-Type: text/plain; charset=UTF-8',
		'Reply-To: ' . str_replace( array( "\r", "\n" ), '', $name ) . ' <' . $email . '>',
	);
	$sent = wp_mail( PP_CONTACT_TO, $subject, $body . "\n\n—\nSent from the contact form on primordial-protocol.com", $headers );

	if ( $id && ! is_wp_error( $id ) ) {
		update_post_meta( $id, '_pp_mail_sent', $sent ? '1' : '0' );
	}

	return array( 'ok' => true );
}

/* ---------- Shortcode ---------- */

add_shortcode( 'pp_contact_form', function () {
	$file = get_stylesheet_directory() . '/assets/js/contact.js';
	wp_enqueue_script( 'primordial-contact', get_stylesheet_directory_uri() . '/assets/js/contact.js', array(), (string) filemtime( $file ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
	wp_localize_script( 'primordial-contact', 'ppContact', array(
		'token' => esc_url_raw( rest_url( 'pp/v1/contact-token' ) ),
		'send'  => esc_url_raw( rest_url( 'pp/v1/contact' ) ),
	) );

	$options = '<option value="" disabled selected>Choose a topic</option>';
	foreach ( pp_contact_topics() as $value => $label ) {
		$options .= sprintf( '<option value="%s">%s</option>', esc_attr( $value ), esc_html( $label ) );
	}

	ob_start();
	?>
	<form class="pp-form" novalidate data-pp-contact>
		<div class="pp-form-row">
			<p class="pp-field">
				<label for="pp-name">Name</label>
				<input id="pp-name" name="name" type="text" autocomplete="name" required maxlength="100">
			</p>
			<p class="pp-field">
				<label for="pp-email">Email</label>
				<input id="pp-email" name="email" type="email" autocomplete="email" required maxlength="200">
			</p>
		</div>
		<div class="pp-form-row">
			<p class="pp-field">
				<label for="pp-topic">Topic</label>
				<select id="pp-topic" name="topic" required><?php echo $options; // phpcs:ignore -- escaped above. ?></select>
			</p>
			<p class="pp-field">
				<label for="pp-org">Organization <span>(optional)</span></label>
				<input id="pp-org" name="org" type="text" autocomplete="organization" maxlength="150">
			</p>
		</div>
		<p class="pp-field">
			<label for="pp-message">Message</label>
			<textarea id="pp-message" name="message" rows="7" required maxlength="5000" placeholder="A few lines on what you have in mind: dates, number of people, goals…"></textarea>
		</p>
		<p class="pp-hp" aria-hidden="true">
			<label for="pp-website">Leave this field empty</label>
			<input id="pp-website" name="website" type="text" tabindex="-1" autocomplete="off">
		</p>
		<div class="pp-form-foot">
			<button type="submit" class="wp-element-button">Send message</button>
			<p class="pp-form-note">Your details are used only to reply to you. See the <a href="/privacy-policy/">Privacy Policy</a>.</p>
		</div>
		<p class="pp-form-status" role="status" aria-live="polite"></p>
		<noscript><p class="pp-form-status is-error">The form needs JavaScript to keep spam out. You can also write to <?php echo antispambot( PP_CONTACT_TO ); // phpcs:ignore ?>.</p></noscript>
	</form>
	<?php
	return ob_get_clean();
} );
