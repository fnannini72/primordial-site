<?php
/**
 * Newsletter signup: Kit form "SITE – Newsletter" (double opt-in), then weekly import to Substack.
 * Shortcode [pp_newsletter]. Our own markup posts straight to Kit's public form endpoint,
 * so no third-party script loads until someone actually subscribes.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const PP_KIT_FORM_ID = '10068216';

add_shortcode( 'pp_newsletter', function () {
	$file = get_stylesheet_directory() . '/assets/js/newsletter.js';
	wp_enqueue_script( 'primordial-newsletter', get_stylesheet_directory_uri() . '/assets/js/newsletter.js', array(), (string) filemtime( $file ), array( 'in_footer' => true, 'strategy' => 'defer' ) );

	static $n = 0;
	$n++;
	$id     = 'pp-news-email-' . $n;
	$action = 'https://app.kit.com/forms/' . PP_KIT_FORM_ID . '/subscriptions';

	ob_start();
	?>
	<form class="pp-news" action="<?php echo esc_url( $action ); ?>" method="post" data-pp-news novalidate>
		<div class="pp-news-row">
			<label class="screen-reader-text" for="<?php echo esc_attr( $id ); ?>">Email address</label>
			<input id="<?php echo esc_attr( $id ); ?>" class="pp-news-input" name="email_address" type="email" autocomplete="email" inputmode="email" placeholder="Your email address" required>
			<button type="submit" class="pp-news-btn">Subscribe</button>
		</div>
		<p class="pp-news-note">Free essays on our ancient biology in a modern world. Delivered by Substack. Unsubscribe anytime.</p>
		<p class="pp-news-status" role="status" aria-live="polite"></p>
		<p class="pp-news-fine"><a href="/privacy-policy/">Privacy</a> · <a href="https://kit.com/features/forms?utm_campaign=poweredby&amp;utm_content=form&amp;utm_medium=referral&amp;utm_source=dynamic" rel="noopener" target="_blank">Built with Kit</a></p>
	</form>
	<?php
	return ob_get_clean();
} );

// The welcome page is a destination after confirming, not something to rank.
add_filter( 'wp_robots', function ( $robots ) {
	if ( is_page( array( 'welcome', 'newsletter-test' ) ) ) {
		$robots['noindex'] = true;
		$robots['follow']  = true;
	}
	return $robots;
} );

// Keep the welcome page out of the XML sitemap.
add_filter( 'wp_sitemaps_posts_query_args', function ( $args, $post_type ) {
	if ( 'page' === $post_type ) {
		$welcome = get_page_by_path( 'welcome' );
		if ( $welcome ) {
			$args['post__not_in'] = array_merge( isset( $args['post__not_in'] ) ? (array) $args['post__not_in'] : array(), array( $welcome->ID ) );
		}
	}
	return $args;
}, 10, 2 );
