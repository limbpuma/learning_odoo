/**
 * Account Selector Dropdown Toggle
 * Handles opening/closing the dropdown menu in SM/MD breakpoints
 */

(function() {
    'use strict';

    function initAccountSelector() {
        try {
            const selectors = document.querySelectorAll('[data-toggle="account-dropdown"]');

            if (selectors.length === 0) return;

            selectors.forEach(function(button) {
                const wrapper = button.closest('.tts-account-selector-wrapper');

                if (!wrapper) return;

                // Toggle dropdown on button click
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    wrapper.classList.toggle('is-expanded');
                });

                // Close dropdown when clicking outside
                document.addEventListener('click', function(e) {
                    if (!wrapper.contains(e.target)) {
                        wrapper.classList.remove('is-expanded');
                    }
                });

                // Close dropdown on Escape key
                document.addEventListener('keydown', function(e) {
                    if (e.key === 'Escape') {
                        wrapper.classList.remove('is-expanded');
                    }
                });
            });
        } catch (error) {
            console.error('Account selector initialization error:', error);
        }
    }

    // Initialize on DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAccountSelector);
    } else {
        // DOM already loaded
        initAccountSelector();
    }
})();
