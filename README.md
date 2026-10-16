# Primordial Protocol — WordPress child theme

Child theme of **Twenty Twenty-Five** for [primordial-protocol.com](https://www.primordial-protocol.com).

- `theme.json` — palette, typography (Montserrat + Literata, self-hosted), spacing, block styles
- `style.css` — theme header + custom CSS (hero lockup, pillar rows, header/footer)
- `functions.php` — enqueues style.css, removes emoji script, preloads fonts
- `parts/` — header and footer
- `templates/` — front page, landing (no title), standard page
- `assets/` — fonts (woff2, SIL OFL) and logo SVGs

Fonts: Montserrat and Literata, SIL Open Font License 1.1, via Fontsource.

## Deploy

The theme lives in `theme/primordial`. It is installed on WordPress by zipping that folder (top-level folder `primordial/`) and uploading it via Appearance → Themes → Add → Upload, or by Claude through the WordPress admin in the browser.
