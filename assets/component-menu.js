/* Mobile menu component */
(function() {
  'use strict';

  class MobileMenu {
    constructor(element, options = {}) {
      this.el = element;
      this.isOpen = false;
    }

    open() {
      this.isOpen = true;
      this.el.removeAttribute('hidden');
      this.el.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    close() {
      this.isOpen = false;
      this.el.setAttribute('hidden', '');
      this.el.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    toggle() {
      this.isOpen ? this.close() : this.open();
    }
  }

  window.Theme = window.Theme || {};
  window.Theme.components = window.Theme.components || {};
  window.Theme.components['mobile-menu'] = MobileMenu;
})();
