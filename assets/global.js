/* global.js — PSI BOT theme core
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
