(function () {
    "use strict";
    function initTechflex() {
        const body = document.body;
        const mobileToggle = document.querySelector('.tf-mobile-toggle');
        const searchToggle = document.querySelector('.tf-search-toggle');
        if (mobileToggle) {
            mobileToggle.addEventListener('click', function () {
                const open = body.classList.toggle('tf-mobile-menu-open');
                mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            });
            document.querySelectorAll('.tf-mobile-nav a').forEach(function (link) {
                link.addEventListener('click', function () {
                    body.classList.remove('tf-mobile-menu-open');
                    mobileToggle.setAttribute('aria-expanded', 'false');
                });
            });
        }
        if (searchToggle) {
            searchToggle.addEventListener('click', function () {
                body.classList.toggle('tf-search-open');
                const input = document.querySelector('.tf-search-panel input');
                if (body.classList.contains('tf-search-open') && input) {
                    window.setTimeout(function () { input.focus(); }, 100);
                }
            });
        }
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTechflex);
    } else {
        initTechflex();
    }
})();
