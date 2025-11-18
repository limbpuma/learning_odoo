// ============================================================================
// CHECKOUT ADDRESS - Billing/Shipping Toggle Functionality
// ============================================================================
// Handles the checkbox toggle for "My shipping address is the same"
// Shows/hides shipping address form based on checkbox state

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const checkbox = document.getElementById('shipping_same');
        const checkboxIcon = document.getElementById('checkbox-icon');
        const shippingSection = document.querySelector('.tts-checkout-shipping-address');

        if (!checkbox || !shippingSection) {
            console.warn('Checkout address elements not found');
            return;
        }

        // Toggle shipping address visibility when checkbox changes
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                // Hide shipping section
                shippingSection.style.display = 'none';

                // Update checkbox icon
                if (checkboxIcon) {
                    checkboxIcon.src = '/custom_shop_templates/static/src/img/icons/checkbox-checked.svg';
                }

                // Remove required attributes from shipping fields
                setShippingFieldsRequired(false);
            } else {
                // Show shipping section
                shippingSection.style.display = 'flex';

                // Update checkbox icon
                if (checkboxIcon) {
                    checkboxIcon.src = '/custom_shop_templates/static/src/img/icons/checkbox.svg';
                }

                // Add required attributes to shipping fields
                setShippingFieldsRequired(true);
            }
        });

        // Allow clicking on label to toggle checkbox
        const checkboxLabel = document.querySelector('.tts-shipping-checkbox');
        if (checkboxLabel) {
            checkboxLabel.addEventListener('click', function(e) {
                // Prevent default to handle manually
                if (e.target !== checkbox) {
                    e.preventDefault();
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            });
        }

        // Helper function to set/remove required attributes on shipping fields
        function setShippingFieldsRequired(required) {
            const shippingRequiredFields = [
                'shipping_first_name',
                'shipping_last_name',
                'shipping_street',
                'shipping_zip',
                'shipping_city',
                'shipping_country_id'
            ];

            shippingRequiredFields.forEach(function(fieldId) {
                const field = document.getElementById(fieldId);
                if (field) {
                    if (required) {
                        field.setAttribute('required', 'required');
                    } else {
                        field.removeAttribute('required');
                    }
                }
            });
        }

        // Form submission handler - combine first and last name
        const form = document.getElementById('checkout-address-form');
        if (form) {
            form.addEventListener('submit', function(e) {
                // Combine billing first and last name
                const billingFirstName = document.getElementById('billing_first_name');
                const billingLastName = document.getElementById('billing_last_name');

                if (billingFirstName && billingLastName) {
                    // Create hidden 'name' field for Odoo compatibility
                    let nameInput = form.querySelector('input[name="name"]');
                    if (!nameInput) {
                        nameInput = document.createElement('input');
                        nameInput.type = 'hidden';
                        nameInput.name = 'name';
                        form.appendChild(nameInput);
                    }
                    nameInput.value = billingFirstName.value + ' ' + billingLastName.value;
                }

                // If shipping is different, combine shipping first and last name
                if (!checkbox.checked) {
                    const shippingFirstName = document.getElementById('shipping_first_name');
                    const shippingLastName = document.getElementById('shipping_last_name');

                    if (shippingFirstName && shippingLastName) {
                        let shippingNameInput = form.querySelector('input[name="shipping_name"]');
                        if (!shippingNameInput) {
                            shippingNameInput = document.createElement('input');
                            shippingNameInput.type = 'hidden';
                            shippingNameInput.name = 'shipping_name';
                            form.appendChild(shippingNameInput);
                        }
                        shippingNameInput.value = shippingFirstName.value + ' ' + shippingLastName.value;
                    }
                }
            });
        }

        // Initialize: ensure shipping section visibility matches checkbox state
        if (checkbox.checked) {
            shippingSection.style.display = 'none';
            setShippingFieldsRequired(false);
            if (checkboxIcon) {
                checkboxIcon.src = '/custom_shop_templates/static/src/img/icons/checkbox-checked.svg';
            }
        } else {
            shippingSection.style.display = 'flex';
            setShippingFieldsRequired(true);
            if (checkboxIcon) {
                checkboxIcon.src = '/custom_shop_templates/static/src/img/icons/checkbox.svg';
            }
        }
    });
})();
