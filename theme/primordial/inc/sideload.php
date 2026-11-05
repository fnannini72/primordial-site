<?php
/**
 * Admin-only helper: import an image from the old project sites into the Media Library.
 * POST /wp-json/pp/v1/sideload  { "url": "...", "title": "...", "alt": "..." }
 * Restricted to users who can upload files and to the old sites' domains.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'pp/v1', '/sideload', array(
		'methods'             => 'POST',
		'permission_callback' => function () {
			return current_user_can( 'upload_files' );
		},
		'callback'            => function ( WP_REST_Request $req ) {
			$url  = esc_url_raw( (string) $req->get_param( 'url' ) );
			$host = wp_parse_url( $url, PHP_URL_HOST );
			$ok   = array( 'www.mental-survival.com', 'mental-survival.com', 'www.puresurvival.life', 'puresurvival.life', 'i0.wp.com' );
			if ( ! $url || ! in_array( $host, $ok, true ) ) {
				return new WP_Error( 'pp_bad_host', 'Only images from the old project sites can be imported.', array( 'status' => 400 ) );
			}
			require_once ABSPATH . 'wp-admin/includes/media.php';
			require_once ABSPATH . 'wp-admin/includes/file.php';
			require_once ABSPATH . 'wp-admin/includes/image.php';
			$id = media_sideload_image( $url, 0, sanitize_text_field( (string) $req->get_param( 'title' ) ), 'id' );
			if ( is_wp_error( $id ) ) {
				return $id;
			}
			$alt = sanitize_text_field( (string) $req->get_param( 'alt' ) );
			if ( $alt ) {
				update_post_meta( $id, '_wp_attachment_image_alt', $alt );
			}
			$src = wp_get_attachment_image_src( $id, 'large' );
			return array( 'id' => $id, 'url' => wp_get_attachment_url( $id ), 'large' => $src ? $src[0] : '' );
		},
	) );
} );
