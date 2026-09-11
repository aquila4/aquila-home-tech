/* ============================================================
   Aquila Home Tech – Admin JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Sidebar toggle (mobile) ───────────────────────────────
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar   = document.getElementById('adminSidebar');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function (e) {
      if (window.innerWidth < 992 &&
          !sidebar.contains(e.target) &&
          !toggleBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // ── Auto-dismiss flash alerts ─────────────────────────────
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      const bsAlert = new bootstrap.Alert(el);
      bsAlert.close();
    });
  }, 5000);

  // ── Image preview before upload ───────────────────────────
  const imageInput = document.getElementById('image');
  if (imageInput) {
    imageInput.addEventListener('change', function () {
      const file = this.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function (e) {
        let preview = document.getElementById('img-preview');
        if (!preview) {
          preview = document.createElement('img');
          preview.id = 'img-preview';
          preview.className = 'admin-product-thumb-lg mt-2 d-block';
          imageInput.parentNode.appendChild(preview);
        }
        preview.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  // ── Confirm dangerous actions ─────────────────────────────
  // (handled inline via onsubmit attributes in templates)

  // ── Highlight active sidebar link ─────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.admin-nav__link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

});
