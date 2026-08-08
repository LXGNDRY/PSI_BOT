/* Quantity input component */
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
