# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class TTSCheckout(WebsiteSale):
    """
    Custom checkout controller for TTS Website
    Extends WebsiteSale to implement multi-step checkout flow:

    Flow: cart → address → shipping → payment → notes → confirmation

    Routes:
    - /shop/checkout?step=address  (Step 1: Billing/Shipping address)
    - /shop/checkout?step=shipping (Step 2: Shipping method selection)
    - /shop/payment                (Step 3: Payment method selection)
    - /shop/checkout/notes         (Step 4: Order notes + Terms acceptance)
    """

    @http.route(['/shop/checkout'], type='http', auth='public', website=True, sitemap=False)
    def checkout(self, **post):
        """
        Override the standard /shop/checkout route to implement sub-steps.

        Sub-steps:
        - step=address  : Show billing/shipping address forms
        - step=shipping : Show shipping method selection
        - (no step)     : Redirect to step=address (default)

        The standard Odoo checkout combines address + shipping in one page.
        This controller separates them into distinct steps for better UX.
        """
        order = request.website.sale_get_order()

        # Redirect to cart if no order
        if not order or not order.order_line or order.state != 'draft':
            return request.redirect('/shop/cart')

        # Get current step (default to 'address' if not specified)
        current_step = post.get('step', 'address')

        # Validate step value
        if current_step not in ['address', 'shipping']:
            current_step = 'address'

        # ===================================================================
        # STEP 1: ADDRESS
        # ===================================================================
        if current_step == 'address':
            # Get countries and states for form dropdowns
            countries = request.env['res.country'].sudo().search([])
            states = request.env['res.country.state'].sudo().search([])

            # Get partner data
            partner = order.partner_id

            # Prepare values - must include all variables expected by website_sale.checkout
            values = {
                'website_sale_order': order,
                'order': order,  # REQUIRED: website_sale.checkout expects 'order'
                'partner': partner,
                'partner_id': partner.id,
                'countries': countries,
                'states': states,
                'current_step': 'address',
                'errors': {},
                'error_message': [],
                'only_services': order and order.only_services or False,
            }

            # Render checkout template (address section will be shown via t-if)
            return request.render('website_sale.checkout', values)

        # ===================================================================
        # STEP 2: SHIPPING
        # ===================================================================
        elif current_step == 'shipping':
            # Check if address was completed (partner must have address data)
            if not order.partner_id.street or not order.partner_id.city:
                # Redirect back to address step if incomplete
                return request.redirect('/shop/checkout?step=address')

            # Get available shipping carriers
            carriers = request.env['delivery.carrier'].sudo().search([])

            # Prepare values - must include all variables expected by website_sale.checkout
            values = {
                'website_sale_order': order,
                'order': order,  # REQUIRED: website_sale.checkout expects 'order'
                'partner': order.partner_id,
                'partner_id': order.partner_id.id,
                'partner_shipping_id': order.partner_shipping_id,
                'carriers': carriers,
                'current_step': 'shipping',
                'errors': {},
                'error_message': [],
                'only_services': order and order.only_services or False,
            }

            # Render checkout template (shipping section will be shown via t-if)
            return request.render('website_sale.checkout', values)

    @http.route(['/shop/checkout/address'], type='http', auth='public', methods=['POST'], website=True, sitemap=False)
    def checkout_address_submit(self, **post):
        """
        Process address form submission (Step 1)

        POST data expected:
        - billing_first_name, billing_last_name
        - company_name, vat
        - billing_street, billing_street2
        - billing_zip, billing_city
        - billing_country_id, billing_state_id
        - phone
        - shipping_same (checkbox: 1 if same as billing)
        - shipping_* fields (if shipping_same != 1)

        Returns: Redirect to /shop/checkout?step=shipping
        """
        order = request.website.sale_get_order()

        if not order:
            return request.redirect('/shop/cart')

        # Get or create billing partner
        partner = order.partner_id

        # Update billing address
        billing_data = {
            'name': f"{post.get('billing_first_name', '')} {post.get('billing_last_name', '')}".strip(),
            'street': post.get('billing_street', ''),
            'street2': post.get('billing_street2', ''),
            'city': post.get('billing_city', ''),
            'zip': post.get('billing_zip', ''),
            'country_id': int(post.get('billing_country_id')) if post.get('billing_country_id') else False,
            'state_id': int(post.get('billing_state_id')) if post.get('billing_state_id') else False,
            'phone': post.get('phone', ''),
            'company_name': post.get('company_name', ''),
            'vat': post.get('vat', ''),
        }

        partner.sudo().write(billing_data)

        # Handle shipping address
        if post.get('shipping_same') == '1':
            # Shipping same as billing
            order.partner_shipping_id = partner
        else:
            # Create or update separate shipping address
            shipping_data = {
                'name': f"{post.get('shipping_first_name', '')} {post.get('shipping_last_name', '')}".strip(),
                'street': post.get('shipping_street', ''),
                'street2': post.get('shipping_street2', ''),
                'city': post.get('shipping_city', ''),
                'zip': post.get('shipping_zip', ''),
                'country_id': int(post.get('shipping_country_id')) if post.get('shipping_country_id') else False,
                'state_id': int(post.get('shipping_state_id')) if post.get('shipping_state_id') else False,
                'type': 'delivery',
                'parent_id': partner.id,
            }

            # Check if shipping address already exists
            if order.partner_shipping_id and order.partner_shipping_id.id != partner.id:
                order.partner_shipping_id.sudo().write(shipping_data)
            else:
                shipping_partner = request.env['res.partner'].sudo().create(shipping_data)
                order.partner_shipping_id = shipping_partner

        # Redirect to shipping step
        return request.redirect('/shop/checkout?step=shipping')

    @http.route(['/shop/checkout/shipping'], type='http', auth='public', methods=['POST'], website=True, sitemap=False)
    def checkout_shipping_submit(self, **post):
        """
        Process shipping method selection (Step 2)

        POST data expected:
        - carrier_id: ID of selected delivery carrier

        Returns: Redirect to /shop/payment
        """
        order = request.website.sale_get_order()

        if not order:
            return request.redirect('/shop/cart')

        # Get selected carrier
        carrier_id = int(post.get('carrier_id', 0))

        if carrier_id:
            # Get carrier object
            carrier = request.env['delivery.carrier'].sudo().browse(carrier_id)

            # Calculate delivery price
            try:
                price_result = carrier.get_delivery_price(order)
                if price_result and 'price' in price_result:
                    delivery_price = price_result['price']
                else:
                    delivery_price = 0

                # Apply carrier and delivery cost to order (Odoo 18 method)
                order.set_delivery_line(carrier, delivery_price)
            except Exception as e:
                # If delivery calculation fails, just set carrier without price
                import logging
                _logger = logging.getLogger(__name__)
                _logger.warning(f"Error calculating delivery price: {str(e)}")
                order.carrier_id = carrier

        # Redirect to payment step
        return request.redirect('/shop/payment')

    @http.route(['/shop/payment'], type='http', auth='public', website=True, sitemap=False)
    def payment(self, **post):
        """
        Override /shop/payment to implement custom payment step with conditionals.

        This renders the same checkout template but with current_step='payment'
        which triggers the payment section in checkout_steps.xml
        """
        order = request.website.sale_get_order()

        # Redirect to cart if no order
        if not order or not order.order_line or order.state != 'draft':
            return request.redirect('/shop/cart')

        # Check if previous steps completed
        if not order.partner_id.street or not order.partner_id.city:
            # Redirect back to address if incomplete
            return request.redirect('/shop/checkout?step=address')

        if not order.carrier_id:
            # Redirect back to shipping if not selected
            return request.redirect('/shop/checkout?step=shipping')

        # Get payment methods
        payment_methods = request.env['payment.method'].sudo().search([])

        # Prepare values for payment step
        values = {
            'website_sale_order': order,
            'order': order,
            'partner': order.partner_id,
            'partner_id': order.partner_id.id,
            'payment_methods_sudo': payment_methods,
            'current_step': 'payment',
            'errors': {},
            'error_message': [],
            'only_services': order and order.only_services or False,
        }

        # Render checkout template (payment section will be shown via t-elif)
        return request.render('website_sale.checkout', values)

    @http.route(['/shop/checkout/payment'], type='http', auth='public', methods=['POST'], website=True, sitemap=False)
    def checkout_payment_submit(self, **post):
        """
        Process payment method selection (Step 3)

        POST data expected:
        - payment_method_id: ID of selected payment method

        Returns: Redirect to /shop/checkout/notes
        """
        order = request.website.sale_get_order()

        if not order:
            return request.redirect('/shop/cart')

        # Get selected payment method
        payment_method_id = int(post.get('payment_method_id', 0))

        if payment_method_id:
            # Store payment method in session for later use
            request.session['selected_payment_method_id'] = payment_method_id

        # Redirect to notes step
        return request.redirect('/shop/checkout/notes')

    @http.route(['/shop/checkout/notes'], type='http', auth='public', website=True, sitemap=False)
    def checkout_notes(self, **post):
        """
        Display notes step (Step 4) - Final step before order confirmation

        Shows:
        - Summary of address, shipping, payment
        - Order note textarea (optional)
        - Terms & conditions checkbox (required)
        - Buy now button

        Returns: Render checkout template with current_step='notes'
        """
        order = request.website.sale_get_order()

        # Redirect to cart if no order
        if not order or not order.order_line or order.state != 'draft':
            return request.redirect('/shop/cart')

        # Check if previous steps completed
        if not order.partner_id.street or not order.partner_id.city:
            return request.redirect('/shop/checkout?step=address')

        if not order.carrier_id:
            return request.redirect('/shop/checkout?step=shipping')

        # Get selected payment method from session
        selected_payment_method_id = request.session.get('selected_payment_method_id')
        selected_payment_method = None

        if selected_payment_method_id:
            selected_payment_method = request.env['payment.method'].sudo().browse(selected_payment_method_id)

        # Prepare values for notes step
        values = {
            'website_sale_order': order,
            'order': order,
            'partner': order.partner_id,
            'partner_id': order.partner_id.id,
            'selected_payment_method': selected_payment_method,
            'current_step': 'notes',
            'errors': {},
            'error_message': [],
            'only_services': order and order.only_services or False,
        }

        # Render checkout template (notes section will be shown via t-elif)
        return request.render('website_sale.checkout', values)

    @http.route(['/shop/checkout/notes'], type='http', auth='public', methods=['POST'], website=True, sitemap=False)
    def checkout_notes_submit(self, **post):
        """
        Process notes form submission (Step 4 - Final step)

        POST data expected:
        - order_note: Optional order note/instructions
        - terms_accepted: Required checkbox (value = '1')

        Returns: Redirect to payment transaction or order confirmation
        """
        order = request.website.sale_get_order()

        if not order:
            return request.redirect('/shop/cart')

        # Validate terms acceptance
        if not post.get('terms_accepted') == '1':
            # Redirect back with error (TODO: add error message)
            return request.redirect('/shop/checkout/notes')

        # Save order note if provided
        order_note = post.get('order_note', '').strip()
        if order_note:
            order.sudo().write({'note': order_note})

        # Get payment method from session
        payment_method_id = request.session.get('selected_payment_method_id')

        if payment_method_id:
            # Process payment transaction
            # This should redirect to payment provider or confirm order
            return request.redirect(f'/shop/payment/transaction?payment_method_id={payment_method_id}')
        else:
            # If no payment method, just confirm order
            return request.redirect('/shop/confirm_order')
