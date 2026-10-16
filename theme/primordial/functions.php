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
