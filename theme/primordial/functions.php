<?php
/**
 * Primordial Protocol child theme.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Load the child stylesheet (block themes don't enqueue it automatically).
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'primordial-style',
		get_stylesheet_uri(),
		array(),
		(string) filemtime( get_stylesheet_directory() . '/style.css' )
	);
} );

// Home hero slideshow (front page only).
add_action( 'wp_enqueue_scripts', function () {
	if ( is_front_page() ) {
		$file = get_stylesheet_directory() . '/assets/js/hero.js';
		wp_enqueue_script( 'primordial-hero', get_stylesheet_directory_uri() . '/assets/js/hero.js', array(), (string) filemtime( $file ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
	}
} );

// Same styles inside the block editor.
add_action( 'after_setup_theme', function () {
	add_editor_style( 'style.css' );
} );

// Speed: drop the emoji detection script and styles.
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
remove_action( 'admin_print_styles', 'print_emoji_styles' );

// Preload the two fonts used above the fold.
add_action( 'wp_head', function () {
	$base = get_stylesheet_directory_uri() . '/assets/fonts/';
	printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( $base . 'montserrat.woff2' ) );
	printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( $base . 'literata.woff2' ) );
}, 1 );

// Keep the old slideshow link working: it now lives on GitHub Pages.
add_action( 'template_redirect', function () {
	$path = isset( $_SERVER['REQUEST_URI'] ) ? strtok( $_SERVER['REQUEST_URI'], '?' ) : '';
	if ( preg_match( '#^/links/evolutionary_mismatch(\.html)?/?$#', $path ) ) {
		wp_redirect( 'https://fnannini72.github.io/ancient-body-timeline/', 301 );
		exit;
	}
}, 1 );

/**
 * [pp_substack_feed limit="6"]
 * Latest Substack posts from the public archive API, including podcast episodes
 * (their artwork is missing from the RSS feed). Cached for 30 minutes.
 */
add_shortcode( 'pp_substack_feed', function ( $atts ) {
	$atts  = shortcode_atts( array( 'limit' => 6 ), $atts, 'pp_substack_feed' );
	$limit = max( 1, min( 12, (int) $atts['limit'] ) );
	$key   = 'pp_substack_feed_' . $limit;
	$posts = get_transient( $key );

	if ( false === $posts ) {
		$res = wp_remote_get(
			'https://primordialprotocol.substack.com/api/v1/archive?sort=new&limit=' . $limit,
			array( 'timeout' => 8, 'headers' => array( 'Accept' => 'application/json' ) )
		);
		$posts = array();
		if ( ! is_wp_error( $res ) && 200 === wp_remote_retrieve_response_code( $res ) ) {
			$data = json_decode( wp_remote_retrieve_body( $res ), true );
			if ( is_array( $data ) ) {
				foreach ( $data as $p ) {
					$img = '';
					if ( ! empty( $p['cover_image'] ) ) {
						$img = $p['cover_image'];
					} elseif ( ! empty( $p['podcast_episode_image_url'] ) ) {
						$img = $p['podcast_episode_image_url'];
					}
					if ( $img && false === strpos( $img, 'substackcdn.com/image/fetch' ) ) {
						$img = 'https://substackcdn.com/image/fetch/w_640,h_360,c_fill,f_auto,q_auto:good/' . rawurlencode( $img );
					}
					$posts[] = array(
						'title' => isset( $p['title'] ) ? $p['title'] : '',
						'url'   => isset( $p['canonical_url'] ) ? $p['canonical_url'] : '',
						'date'  => isset( $p['post_date'] ) ? $p['post_date'] : '',
						'text'  => ! empty( $p['subtitle'] ) ? $p['subtitle'] : ( isset( $p['description'] ) ? $p['description'] : '' ),
						'img'   => $img,
						'kind'  => ( isset( $p['type'] ) && 'podcast' === $p['type'] ) ? 'Podcast' : '',
						'paid'  => ( isset( $p['audience'] ) && 'everyone' !== $p['audience'] ),
					);
				}
			}
			set_transient( $key, $posts, 30 * MINUTE_IN_SECONDS );
		} else {
			set_transient( $key, $posts, 5 * MINUTE_IN_SECONDS );
		}
	}

	if ( empty( $posts ) ) {
		return '<p><a href="https://primordialprotocol.substack.com/archive">Read the latest posts on Substack</a></p>';
	}

	$out = '<div class="fefs-wrap"><div class="fefs-feed fefs-feed--horizontal">';
	foreach ( $posts as $p ) {
		$meta = array();
		if ( $p['kind'] ) {
			$meta[] = $p['kind'];
		}
		if ( $p['paid'] ) {
			$meta[] = 'Paid';
		}
		if ( $p['date'] ) {
			$meta[] = date_i18n( 'j M Y', strtotime( $p['date'] ) );
		}
		$out .= '<article class="fefs-card"><a class="fefs-card-link" href="' . esc_url( $p['url'] ) . '" target="_blank" rel="noopener">';
		if ( $p['img'] ) {
			$out .= '<div class="fefs-card-image"><img src="' . esc_url( $p['img'] ) . '" alt="" loading="lazy" decoding="async" width="640" height="360"></div>';
		}
		$out .= '<div class="fefs-card-body"><h3 class="fefs-card-title">' . esc_html( $p['title'] ) . '</h3>';
		$out .= '<div class="fefs-card-date">' . esc_html( implode( ', ', $meta ) ) . '</div>';
		if ( $p['text'] ) {
			$out .= '<p class="fefs-card-excerpt">' . esc_html( wp_trim_words( $p['text'], 24 ) ) . '</p>';
		}
		$out .= '</div></a></article>';
	}
	return $out . '</div></div>';
} );
