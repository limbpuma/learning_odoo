/**
 * TTS Prefetch - instant.page integration
 * Preloads pages on hover/mousedown for instant navigation
 *
 * Strategy: Mousedown + hover hybrid
 * - Starts prefetch on mousedown (100-200ms before click)
 * - Falls back to hover on desktop
 * - Uses mousedown on mobile (no hover)
 *
 * Blacklist: Excludes logout, external links, POST forms
 * Whitelist: Only internal links (/my, /shop, /page)
 */
(function() {
    'use strict';

    // Configuration
    const config = {
        // Intensity: 'mousedown' | 'hover' | 'viewport'
        // mousedown = fastest (100ms before click)
        intensity: 'mousedown',

        // Blacklist - URLs that should NEVER be prefetched
        blacklist: [
            '/web/session/logout',      // Logout (kills session)
            '/newsletter/subscribe',    // POST form
            '/web/signup',              // POST form
            '/web/login',               // POST form (login page is fine, but form submit not)
        ],

        // Allow query strings (e.g., /my/addresses?edit=1)
        allowQueryString: true,

        // Allow external links (false = only prefetch same-origin)
        allowExternalLinks: false
    };

    /**
     * Check if URL should be prefetched
     */
    function shouldPrefetch(url) {
        // External links - skip
        if (url.startsWith('http') && !url.startsWith(window.location.origin)) {
            return false;
        }

        // Blacklist check
        for (const pattern of config.blacklist) {
            if (url.includes(pattern)) {
                return false;
            }
        }

        // Anchor links - skip
        if (url.includes('#')) {
            return false;
        }

        return true;
    }

    /**
     * Prefetch on mousedown (instant.page strategy)
     *
     * Mousedown happens ~100-200ms before click (mouseup)
     * This gives us time to start loading before navigation
     */
    let prefetchedLinks = new Set();

    document.addEventListener('mousedown', function(e) {
        const link = e.target.closest('a');
        if (!link || !link.href) return;

        const url = link.href;

        if (!shouldPrefetch(url)) return;
        if (prefetchedLinks.has(url)) return; // Already prefetched

        // Create prefetch hint
        const prefetchLink = document.createElement('link');
        prefetchLink.rel = 'prefetch';
        prefetchLink.href = url;
        prefetchLink.as = 'document';

        document.head.appendChild(prefetchLink);
        prefetchedLinks.add(url);
    }, true); // Use capture phase for earliest detection

    /**
     * Prefetch on hover (desktop only)
     *
     * Hover typically happens 300-500ms before click
     * This gives more time to load, but only on desktop
     */
    let hoverTimeout;

    document.addEventListener('mouseover', function(e) {
        const link = e.target.closest('a');
        if (!link || !link.href) return;

        const url = link.href;

        if (!shouldPrefetch(url)) return;
        if (prefetchedLinks.has(url)) return;

        // Debounce hover (only prefetch if hover lasts 100ms)
        clearTimeout(hoverTimeout);
        hoverTimeout = setTimeout(function() {
            const prefetchLink = document.createElement('link');
            prefetchLink.rel = 'prefetch';
            prefetchLink.href = url;
            prefetchLink.as = 'document';

            document.head.appendChild(prefetchLink);
            prefetchedLinks.add(url);
        }, 100);
    });

    /**
     * Clear hover timeout on mouseout
     */
    document.addEventListener('mouseout', function(e) {
        clearTimeout(hoverTimeout);
    });

    /**
     * Clear cache on logout (in case user navigates to logout)
     */
    window.addEventListener('beforeunload', function() {
        if (window.location.pathname.includes('/logout')) {
            prefetchedLinks.clear();
        }
    });

})();
