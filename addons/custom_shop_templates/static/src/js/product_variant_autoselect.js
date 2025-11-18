/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { WebsiteSale } from '@website_sale/js/website_sale';

patch(WebsiteSale.prototype, {

    /**
     * Override _openDialog to skip all configurator checks.
     *
     * Original flow:
     *   1. Check for combos → open combo configurator
     *   2. Check shouldShowProductConfigurator → open product configurator
     *   3. Otherwise → submit form
     *
     * MVP flow:
     *   - Skip all checks and go directly to form submission
     */
    async _openDialog(isOnProductPage) {
        console.log('[TTS MVP] Skipping product configurator - adding directly to cart');

        // Skip all configurator logic and submit the form directly
        // This will add the product to cart with the currently selected variant
        // (or the first variant if none is explicitly selected)
        return this._submitForm();
    },

});
