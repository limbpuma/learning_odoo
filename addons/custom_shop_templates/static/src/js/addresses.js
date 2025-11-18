/**
 * TTS Addresses - Toggle between list view and form view
 * Allows editing addresses without reloading the page
 */
(function() {
    'use strict';

    function initAddressesToggle() {
        // Get view containers
        const listView = document.querySelector('[data-view="list"]');
        const formView = document.querySelector('[data-view="form"]');

        if (!listView || !formView) {
            return; // Not on addresses page
        }

        /**
         * Show form view, hide list view
         */
        function showForm(e) {
            if (e) {
                e.preventDefault();
            }

            // Hide list, show form
            listView.style.display = 'none';
            formView.style.display = 'block';

            // Update URL without reloading
            history.pushState({ view: 'form' }, '', '/my/addresses/edit');
        }

        /**
         * Show list view, hide form view
         */
        function showList(e) {
            if (e) {
                e.preventDefault();
            }

            // Hide form, show list
            formView.style.display = 'none';
            listView.style.display = 'block';

            // Update URL without reloading
            history.pushState({ view: 'list' }, '', '/my/addresses');
        }

        // Attach click handlers to all "Edit" buttons (show form)
        const editButtons = document.querySelectorAll('[data-action="show-form"]');
        editButtons.forEach(function(btn) {
            btn.addEventListener('click', showForm);
        });

        // Attach click handler to "Cancel" button (show list)
        const cancelBtn = document.querySelector('[data-action="show-list"]');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', showList);
        }

        // Handle browser back/forward buttons
        window.addEventListener('popstate', function(event) {
            if (event.state && event.state.view === 'form') {
                // Show form without animation
                listView.style.display = 'none';
                formView.style.display = 'block';
            } else {
                // Show list
                formView.style.display = 'none';
                listView.style.display = 'block';
            }
        });

        // Initialize state on page load
        // If URL contains /edit, show form
        if (window.location.pathname === '/my/addresses/edit') {
            showForm();
        }
    }

    // Execute initialization
    // Check if DOM is already loaded (in case script loads after DOMContentLoaded)
    if (document.readyState === 'loading') {
        // DOM not ready yet, wait for it
        document.addEventListener('DOMContentLoaded', initAddressesToggle);
    } else {
        // DOM is already ready, execute now
        initAddressesToggle();
    }
})();
