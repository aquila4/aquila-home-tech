/* ============================================================
   Aquila Home Tech – Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ── AOS (Animate On Scroll) init ──────────────────────────
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 700, once: true, offset: 60 });
  }

  // ── Auto-dismiss flash messages after 5 seconds ───────────
  const flashContainer = document.getElementById('flash-container');
  if (flashContainer) {
    setTimeout(function () {
      flashContainer.querySelectorAll('.alert').forEach(function (alert) {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      });
    }, 5000);
  }

  // ── Navbar scroll effect ──────────────────────────────────
  const navbar = document.querySelector('.aq-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 24px rgba(0,0,0,.3)';
      } else {
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,.2)';
      }
    });
  }

  // ── Smooth scroll for anchor links ────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Product image fallback (handled inline via onerror) ───

  // ── WhatsApp float button pulse ───────────────────────────
  const waFloat = document.querySelector('.whatsapp-float');
  if (waFloat) {
    setInterval(function () {
      waFloat.style.transform = 'scale(1.1)';
      setTimeout(function () {
        waFloat.style.transform = 'scale(1)';
      }, 300);
    }, 4000);
  }

});
