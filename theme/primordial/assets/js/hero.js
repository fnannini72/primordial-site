/* Primordial Protocol: home hero slideshow.
   Always opens on the first frame (footprint in volcanic ash), then crossfades
   through images from the "Ancient Body, Modern World" timeline every 30 s.
   No rotation when the visitor prefers reduced motion. */
(function () {
	var hero = document.querySelector('.pp-hero--photo');
	if (!hero) return;
	var base = (document.currentScript && document.currentScript.src || '').replace(/js\/hero\.js.*$/, 'img/hero/');
	var COUNT = 8, HOLD = 30000;
	var mobile = window.matchMedia('(max-width: 781px)');
	var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
	var src = function (i) { var n = (i < 10 ? '0' : '') + i; return base + n + (mobile.matches ? '-m' : '') + '.jpg'; };

	var stage = document.createElement('div');
	stage.className = 'pp-hero-slides';
	stage.setAttribute('aria-hidden', 'true');
	var a = document.createElement('div'), b = document.createElement('div');
	a.className = b.className = 'pp-hero-slide';
	stage.appendChild(a); stage.appendChild(b);
	hero.insertBefore(stage, hero.firstChild);

	var current = 0, front = a, back = b;
	front.style.backgroundImage = 'url("' + src(0) + '")';
	front.classList.add('is-on');
	hero.classList.add('has-slides');

	if (reduce.matches) return;

	function next() {
		if (document.hidden) { return setTimeout(next, HOLD); }
		var i = (current + 1) % COUNT, img = new Image();
		img.onload = function () {
			back.style.backgroundImage = 'url("' + img.src + '")';
			back.classList.add('is-on');
			front.classList.remove('is-on');
			var t = front; front = back; back = t;
			current = i;
			setTimeout(next, HOLD);
		};
		img.onerror = function () { current = i; setTimeout(next, 1000); };
		img.src = src(i);
	}
	setTimeout(next, HOLD);
})();
