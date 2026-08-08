"""
JS generator — produces global.js and component JS files.
All vanilla JS, no framework, progressive enhancement only.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from ..core.manifest import ThemeManifest


class JSGenerator:
    """Generates all JavaScript asset files."""

    def __init__(self, manifest: "ThemeManifest"):
        self.manifest = manifest

    def generate(self) -> Dict[str, str]:
        """Generate all JS files. Returns dict of path -> content."""
        files: Dict[str, str] = {}
        files["assets/global.js"] = self._global_js()
        files["assets/component-cart.js"] = self._cart_js()
        files["assets/component-menu.js"] = self._menu_js()
        files["assets/component-variants.js"] = self._variants_js()
        files["assets/component-quantity.js"] = self._quantity_js()
        files["assets/component-search.js"] = self._search_js()
        return files

    def _global_js(self) -> str:
        """Global init, event bus, lazy loader."""
        return """/* global.js — PSI BOT theme core
 * Progressive enhancement only. No framework.
 */
(function() {
  'use strict';

  // -------------------------------------------------------------------------
  // Event bus (pub/sub)
  // -------------------------------------------------------------------------
  const bus = {
    _events: {},
    on(event, cb) {
      (this._events[event] = this._events[event] || []).push(cb);
    },
    emit(event, data) {
      (this._events[event] || []).forEach(cb => cb(data));
    },
    off(event, cb) {
      const arr = this._events[event];
      if (!arr) return;
      const idx = arr.indexOf(cb);
      if (idx > -1) arr.splice(idx, 1);
    }
  };

  // -------------------------------------------------------------------------
  // Utility helpers
  // -------------------------------------------------------------------------
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  // -------------------------------------------------------------------------
  // Lazy component hydration via IntersectionObserver
  // -------------------------------------------------------------------------
  const loadedComponents = new Set();

  function loadComponent(name, element) {
    if (loadedComponents.has(name + ':' + element)) return;
    loadedComponents.add(name + ':' + element);

    const script = document.createElement('script');
    script.src = window.themeAssets['component-' + name + '.js'] ||
                 document.querySelector('[href*="component-' + name + '"]')?.src?.replace('.css', '.js') || '';
    script.defer = true;
    script.onload = () => {
      if (window.Theme && window.Theme.components && window.Theme.components[name]) {
        new window.Theme.components[name](element, element.dataset.options ? JSON.parse(element.dataset.options) : {});
      }
    };
    if (script.src) document.head.appendChild(script);
  }

  const componentObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const name = el.dataset.component;
        if (name) loadComponent(name, el);
        componentObserver.unobserve(el);
      }
    });
  }, { rootMargin: '200px' });

  function initComponents() {
    $$('[data-component]').forEach(el => componentObserver.observe(el));
  }

  // -------------------------------------------------------------------------
  // Above-the-fold components (hydrate immediately)
  // -------------------------------------------------------------------------
  function initAboveFold() {
    // Header is always above the fold
    const header = document.querySelector('.header');
    if (header) {
      // Header JS comes from section js tag
    }
  }

  // -------------------------------------------------------------------------
  // Expose to window
  // -------------------------------------------------------------------------
  window.Theme = window.Theme || {};
  window.Theme.bus = bus;
  window.Theme.$ = $;
  window.Theme.$$ = $$;

  // -------------------------------------------------------------------------
  // Boot
  // -------------------------------------------------------------------------
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initAboveFold();
      initComponents();
    });
  } else {
    initAboveFold();
    initComponents();
  }
})();
"""

    def _cart_js(self) -> str:
        return """/* Cart component */
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
"""

    def _menu_js(self) -> str:
        return """/* Mobile menu component */
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
"""

    def _variants_js(self) -> str:
        return """/* Product variant picker */
(function() {
  'use strict';

  class VariantPicker {
    constructor(element, options = {}) {
      this.el = element;
      this.product = options.product || null;
      this.selectedOptions = [];
      this.bindEvents();
    }

    bindEvents() {
      const buttons = this.el.querySelectorAll('[data-option-index]');
      buttons.forEach(btn => {
        btn.addEventListener('click', (e) => {
          const index = parseInt(btn.dataset.optionIndex);
          const value = btn.dataset.value;
          this.selectOption(index, value, btn);
        });
      });
    }

    selectOption(index, value, button) {
      // Update UI
      const siblings = button.parentElement.querySelectorAll('[data-option-index]');
      siblings.forEach(s => s.setAttribute('aria-selected', 'false'));
      button.setAttribute('aria-selected', 'true');

      this.selectedOptions[index] = value;
      this.updateVariant();
    }

    updateVariant() {
      if (!this.product || !this.product.variants) return;

      const variant = this.product.variants.find(v =>
        v.options.every((opt, i) => opt === this.selectedOptions[i])
      );

      if (variant) {
        window.Theme?.bus.emit('variant:change', variant);
        // Update hidden input
        const variantInput = this.el.closest('form')?.querySelector('[name="id"]');
        if (variantInput) variantInput.value = variant.id;
      }
    }
  }

  window.Theme = window.Theme || {};
  window.Theme.components = window.Theme.components || {};
  window.Theme.components['variant-picker'] = VariantPicker;
})();
"""

    def _quantity_js(self) -> str:
        return """/* Quantity input component */
(function() {
  'use strict';

  function initQuantityInputs() {
    document.querySelectorAll('[data-quantity-input]').forEach(wrapper => {
      const input = wrapper.querySelector('input');
      const decrease = wrapper.querySelector('[data-action="decrease"]');
      const increase = wrapper.querySelector('[data-action="increase"]');

      function updateButtons() {
        const val = parseInt(input.value) || 1;
        const min = parseInt(input.min) || 1;
        const max = parseInt(input.max) || 999999;
        decrease.disabled = val <= min;
        increase.disabled = val >= max;
      }

      decrease?.addEventListener('click', () => {
        const val = parseInt(input.value) || 1;
        const min = parseInt(input.min) || 1;
        if (val > min) {
          input.value = val - 1;
          updateButtons();
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      });

      increase?.addEventListener('click', () => {
        const val = parseInt(input.value) || 1;
        const max = parseInt(input.max) || 999999;
        if (val < max) {
          input.value = val + 1;
          updateButtons();
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      });

      input.addEventListener('input', updateButtons);
      updateButtons();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initQuantityInputs);
  } else {
    initQuantityInputs();
  }
})();
"""

    def _search_js(self) -> str:
        return """/* Predictive search component */
(function() {
  'use strict';

  class PredictiveSearch {
    constructor(element, options = {}) {
      this.el = element;
      this.input = element.querySelector('input[type="search"]');
      this.results = element.querySelector('[data-search-results]');
      this.debounce = null;
      this.bindEvents();
    }

    bindEvents() {
      this.input?.addEventListener('input', (e) => {
        clearTimeout(this.debounce);
        const query = e.target.value.trim();
        if (query.length < 2) {
          this.hideResults();
          return;
        }
        this.debounce = setTimeout(() => this.search(query), 250);
      });

      // Close on outside click
      document.addEventListener('click', (e) => {
        if (!this.el.contains(e.target)) this.hideResults();
      });

      // Keyboard navigation
      this.input?.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') this.hideResults();
      });
    }

    async search(query) {
      const url = `/search/suggest?q=${encodeURIComponent(query)}&resources[type]=product,collection,page,article&resources[limit]=5`;
      try {
        const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
        const data = await res.json();
        this.renderResults(data);
      } catch (e) {
        console.error('Search failed', e);
      }
    }

    renderResults(data) {
      // Render search results
      this.results?.removeAttribute('hidden');
    }

    hideResults() {
      this.results?.setAttribute('hidden', '');
    }
  }

  window.Theme = window.Theme || {};
  window.Theme.components = window.Theme.components || {};
  window.Theme.components['predictive-search'] = PredictiveSearch;
})();
"""
