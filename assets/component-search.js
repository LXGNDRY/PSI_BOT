/* Predictive search component */
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
