# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class TTSPortal(CustomerPortal):
    """
    Custom portal controller for TTS Website
    Inherits from CustomerPortal to override native Odoo portal routes
    Handles My Account pages: Addresses, Payment Method, Account Details
    """

    @http.route(['/my/addresses', '/my/addresses/edit'], type='http', auth='user', website=True)
    def portal_my_addresses(self, **kw):
        """
        Addresses page - Shows billing and shipping addresses OR edit form
        Routes: /my/addresses (list view) OR /my/addresses/edit (form view)
        Template: custom_shop_templates.portal_my_addresses (contains both views)

        Uses Odoo's standard address_get() method which performs DFS search
        through descendants and ancestors to find invoice/delivery addresses.
        """
        partner = request.env.user.partner_id

        # Use Odoo's standard address_get() method (same as sale_order)
        # Returns dict: {'invoice': id, 'delivery': id}
        # Automatically falls back to 'contact' type or partner itself
        addr_ids = partner.address_get(['invoice', 'delivery'])

        # Browse to get recordsets
        billing_address = request.env['res.partner'].browse(addr_ids['invoice'])
        shipping_address = request.env['res.partner'].browse(addr_ids['delivery'])

        # Only show address if it has actual address data
        if not (billing_address.street or billing_address.city or billing_address.zip):
            billing_address = False

        if not (shipping_address.street or shipping_address.city or shipping_address.zip):
            shipping_address = False

        # Get countries and states for form dropdowns
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        # Determine which view to show based on URL path
        show_form = request.httprequest.path == '/my/addresses/edit'

        values = {
            'partner': partner,
            'billing_address': billing_address,
            'shipping_address': shipping_address,
            'countries': countries,
            'states': states,
            'show_form': show_form,
            'show_success': kw.get('success') == '1',
            'page_name': 'addresses',
        }

        return request.render('custom_shop_templates.portal_my_addresses', values)

    @http.route(['/my/addresses/edit'], type='http', auth='user', website=True)
    def portal_my_addresses_edit(self, **kw):
        """
        Addresses edit page - Form to edit billing address
        Route: /my/addresses/edit
        Template: custom_shop_templates.portal_my_addresses_edit
        """
        partner = request.env.user.partner_id

        # Get countries and states for dropdowns
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values = {
            'partner': partner,
            'countries': countries,
            'states': states,
            'page_name': 'addresses',
        }

        return request.render('custom_shop_templates.portal_my_addresses_edit', values)

    @http.route(['/my/addresses/save'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def portal_addresses_save(self, **post):
        """
        Save addresses form
        Handles POST from /my/addresses form
        """
        partner = request.env.user.partner_id

        # Combine first_name + last_name into name
        first_name = post.get('first_name', '').strip()
        last_name = post.get('last_name', '').strip()
        name = f"{first_name} {last_name}".strip()

        # Update partner address and name
        partner.sudo().write({
            'name': name,
            'street': post.get('street'),
            'street2': post.get('street2'),
            'city': post.get('city'),
            'zip': post.get('zip'),
            'state_id': int(post.get('state_id')) if post.get('state_id') else False,
            'country_id': int(post.get('country_id')),
        })

        # Redirect back to addresses page with success flag
        return request.redirect('/my/addresses?success=1')

    @http.route(['/my/payment_method'], type='http', auth='user', website=True)
    def portal_my_payment_method(self, **kw):
        """
        Payment Method page - Shows saved payment method preference
        Route: /my/payment_method
        Template: custom_shop_templates.portal_my_payment_methods
        """
        partner = request.env.user.partner_id

        values = {
            'partner': partner,
            'page_name': 'payment_method',
            'success': kw.get('success') == '1',
        }

        return request.render('custom_shop_templates.portal_my_payment_methods', values)

    @http.route(['/my/payment_method/save_preference'], type='json', auth='user', methods=['POST'], website=True)
    def save_payment_preference(self, payment_method_code=None):
        """
        Save user's preferred payment method
        JSON endpoint called by JavaScript

        :param payment_method_code: Code of preferred method ('card', 'paypal', 'bank_transfer', 'demo')
        :return: dict with success status
        """
        partner = request.env.user.partner_id

        if payment_method_code:
            partner.sudo().write({
                'preferred_payment_method_code': payment_method_code
            })
            return {'success': True, 'preferred_method': payment_method_code}

        return {'success': False, 'error': 'No payment method code provided'}

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **kw):
        """
        Account Details main page - Shows account info card (read-only)
        Route: /my/account (overrides Odoo native CustomerPortal.account method)
        Template: custom_shop_templates.portal_my_account_details

        Displays: Name, Phone, Email, Display Name, Password last update
        """
        partner = request.env.user.partner_id
        user = request.env.user

        # Get last update date (use write_date as proxy for password change)
        password_write_date = user.write_date or user.create_date

        values = {
            'partner': partner,
            'user': user,
            'password_write_date': password_write_date,
            'page_name': 'account_details',
            'success': kw.get('success') == '1',
        }

        return request.render('custom_shop_templates.portal_my_account_details', values)

    @http.route(['/my/account/edit'], type='http', auth='user', website=True)
    def portal_my_account_details_edit(self, **kw):
        """
        Account Details edit page - Form to edit account information
        Route: /my/account/edit
        Template: custom_shop_templates.portal_my_account_details_edit
        """
        partner = request.env.user.partner_id
        user = request.env.user

        values = {
            'partner': partner,
            'user': user,
            'page_name': 'account_details',
            'error': kw.get('error'),
            'error_message': kw.get('error_message'),
        }

        return request.render('custom_shop_templates.portal_my_account_details_edit', values)

    @http.route(['/my/account/save'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def portal_account_details_save(self, **post):
        """
        Save account details form
        Handles POST from /my/account/edit form

        Fields:
        - first_name, last_name -> combined into 'name'
        - display_name (custom field or computed)
        - company_name -> commercial_company_name
        - vat
        - phone
        - email
        - current_password, new_password, confirm_password (optional)
        """
        partner = request.env.user.partner_id
        user = request.env.user

        # Validate email format
        email = post.get('email', '').strip()
        if email and '@' not in email:
            return request.redirect('/my/account/edit?error=email&error_message=Please enter a valid Email Address.')

        # Combine first_name + last_name into name
        first_name = post.get('first_name', '').strip()
        last_name = post.get('last_name', '').strip()
        name = f"{first_name} {last_name}".strip()

        # Prepare partner values
        partner_values = {
            'name': name,
            'phone': post.get('phone', '').strip(),
            'email': email,
        }

        # Optional fields
        if post.get('company_name'):
            partner_values['commercial_company_name'] = post.get('company_name').strip()

        if post.get('vat'):
            partner_values['vat'] = post.get('vat').strip()

        # Update partner
        partner.sudo().write(partner_values)

        # Handle password change (if provided)
        current_password = post.get('current_password', '').strip()
        new_password = post.get('new_password', '').strip()
        confirm_password = post.get('confirm_password', '').strip()

        if current_password and new_password:
            # Validate passwords match
            if new_password != confirm_password:
                return request.redirect('/my/account/edit?error=password&error_message=New passwords do not match.')

            # Validate current password
            try:
                user._check_credentials(current_password, {'interactive': True})
            except:
                return request.redirect('/my/account/edit?error=password&error_message=Current password is incorrect.')

            # Update password
            user.sudo().write({'password': new_password})

        # Redirect back to account details page with success flag
        return request.redirect('/my/account?success=1')
