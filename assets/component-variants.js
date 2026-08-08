/* Product variant picker */
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
