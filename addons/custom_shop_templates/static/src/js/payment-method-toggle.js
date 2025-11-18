/**
 * TTS Payment Method Toggle - Edit without page reload
 * Allows editing payment method card without reloading the page
 * Based on addresses.js pattern
 */
(function() {
    'use strict';

    function initPaymentMethodToggle() {
        // Get view containers
        const cardView = document.querySelector('[data-view="card"]');
        const formView = document.querySelector('[data-view="form"]');

        if (!cardView && !formView) {
            return; // Not on payment method page
        }

        /**
         * Show form view, hide card view
         */
        function showForm(e) {
            if (e) {
                e.preventDefault();
            }

            // Hide card, show form
            if (cardView) cardView.style.display = 'none';
            if (formView) formView.style.display = 'block';

            // Update URL without reloading
            history.pushState({ view: 'form' }, '', '/my/payment_method?edit=1');
        }

        // Attach click handlers to all "Edit" buttons (show form)
        const editButtons = document.querySelectorAll('[data-action="show-form"]');
        editButtons.forEach(function(btn) {
            btn.addEventListener('click', showForm);
        });

        // Handle browser back/forward buttons
        window.addEventListener('popstate', function(event) {
            if (event.state && event.state.view === 'form') {
                // Show form
                if (cardView) cardView.style.display = 'none';
                if (formView) formView.style.display = 'block';
            } else {
                // Show card
                if (formView) formView.style.display = 'none';
                if (cardView) cardView.style.display = 'block';
            }
        });

        // Initialize state on page load
        // If URL contains edit=1, show form
        if (window.location.search.includes('edit=1')) {
            showForm();
        }
    }

    // Execute initialization
    // Check if DOM is already loaded (in case script loads after DOMContentLoaded)
    if (document.readyState === 'loading') {
        // DOM not ready yet, wait for it
        document.addEventListener('DOMContentLoaded', initPaymentMethodToggle);
    } else {
        // DOM is already ready, execute now
        initPaymentMethodToggle();
    }
})();
