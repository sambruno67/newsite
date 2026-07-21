document.addEventListener('DOMContentLoaded', function () {

  // ── Burger menu mobile ─────────────────────────────────────────
  const burger      = document.getElementById('burger');
  const mobileMenu  = document.getElementById('mobile-menu');

  if (burger && mobileMenu) {
    burger.addEventListener('click', function () {
      const isOpen = !mobileMenu.classList.contains('-translate-x-full');

      if (isOpen) {
        // Fermer
        mobileMenu.classList.add('-translate-x-full');
        burger.setAttribute('aria-expanded', 'false');
      } else {
        // Ouvrir
        mobileMenu.classList.remove('-translate-x-full');
        burger.setAttribute('aria-expanded', 'true');
      }
    });

    // Fermer en cliquant sur un lien
    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileMenu.classList.add('-translate-x-full');
        burger.setAttribute('aria-expanded', 'false');
      });
    });

    // Fermer en cliquant en dehors
    document.addEventListener('click', function (e) {
      if (!burger.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.add('-translate-x-full');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── Navbar scroll ──────────────────────────────────────────────
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 20) {
        navbar.classList.add('shadow-lg', 'shadow-navy/20');
      } else {
        navbar.classList.remove('shadow-lg', 'shadow-navy/20');
      }
    });
  }

});