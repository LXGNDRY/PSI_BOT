/* Cart component */
(function() {
  'use strict';

  class CartDrawer {
    constructor(element, options = {}) {
      this.el = element;
      this.isOpen = false;
      this.bindEvents();
    }

    bindEvents() {
      const closeBtn = this.el.querySelector('[data-action="close"]');
      closeBtn?.addEventListener('click', () => this.close());

      // Close on backdrop click
      this.el.addEventListener('click', (e) => {
        if (e.target === this.el) this.close();
      });

      // Close on escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isOpen) this.close();
      });

      // Cart add success
      document.addEventListener('cart:added', () => {
        this.open();
        this.rerender();
      });
    }

    open() {
      this.isOpen = true;
      this.el.removeAttribute('hidden');
      this.el.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      window.Theme?.bus.emit('cart:open');
    }

    close() {
      this.isOpen = false;
      this.el.setAttribute('hidden', '');
      this.el.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      window.Theme?.bus.emit('cart:close');
    }

    async rerender() {
      const url = '/cart?sections=cart-drawer';
      try {
        const res = await fetch(url);
        const data = await res.json();
        // ... replace content
      } catch (e) {
        console.error('Cart rerender failed', e);
      }
    }

    async addItem(variantId, quantity = 1) {
      const res = await fetch('/cart/add.js', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ id: variantId, quantity })
      });

      if (res.ok) {
        window.Theme?.bus.emit('cart:added', await res.json());
        return true;
      }
      const err = await res.json();
      window.Theme?.bus.emit('cart:error', err);
      return false;
    }
  }

  window.Theme = window.Theme || {};
  window.Theme.components = window.Theme.components || {};
  window.Theme.components['cart-drawer'] = CartDrawer;
})();
