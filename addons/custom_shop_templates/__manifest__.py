# -*- coding: utf-8 -*-
{
    'name': 'TTS Custom Shop Templates',
    'version': '18.0.0.1.0',
    'summary': 'Custom e-commerce templates that replace Odoo defaults with branded designs',
    'description': """
        Custom shop templates for a better-looking Odoo e-commerce experience.

        What you get:
        - Complete customer account area (dashboard, orders, addresses, payment settings)
        - Custom login and registration pages
        - Product catalog, detail pages, and shopping cart
        - Responsive design that works on phones, tablets, and desktops
        - Built with Bootstrap 5 and modular SCSS for easy customization

        Current status:
        Account portal is 90% done, authentication pages are complete, shop templates
        have basic implementations. Checkout flow coming next.

        Technical stuff:
        Uses component-based templates, modular SCSS with brand variables, and page-specific
        styling. Integrates with Odoo's portal and e-commerce modules. BentonSans font included.

        Requires Odoo 18.0+, website, website_sale, and portal modules.
    """,
    'author': 'TTS Team',
    'website': 'https://www.my-website.com',
    'category': 'Website/Theme',
    'depends': [
        'base',
        'website',
        'website_sale',
        'portal',
        'sale',
        'stock',  # For product inventory
        'account',
        'auth_signup',
        'payment',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Configuration
        'data/website.xml',
        'data/images.xml',

        # Layout (header, footer, base)
        'views/layout/assets.xml',
        'views/layout/base_layout.xml',
        'views/layout/header_navbar.xml',
        'views/layout/footer.xml',

        # Reusable components
        'views/components/breadcrumb_trail.xml',
        'views/components/page_title.xml',
        'views/components/product_card.xml',
        'views/components/shop_search_filter.xml',
        'views/components/product_results_info.xml',
        'views/components/button_halftone.xml',
        'views/components/article_narrow.xml',
        'views/components/faq_section.xml',
        'views/components/reseller_section.xml',
        'views/components/quantity_selector.xml',
        'views/components/related_products_detail.xml',
        'views/components/account_navigation.xml',
        'views/components/account_page_layout.xml',
        'views/components/banner_alert.xml',
        # 'views/components/checkout_page_layout.xml',  # DISABLED: Not used, checkout_steps.xml handles layout

        # Shop pages
        'views/shop/shop_products.xml',
        'views/shop/shop_related_products.xml',
        'views/shop/shop_product_detail.xml',
        #'views/shop/shop_cart.xml',

        # Checkout flow
        'views/checkout/checkout_cart.xml',
        'views/checkout/checkout_steps.xml',      # Complete checkout flow: address → shipping → payment → notes
        # 'views/checkout/checkout_payment.xml',  # DISABLED: Payment now handled in checkout_steps.xml (lines 597-688)

        # Authentication
        'views/account/login.xml',
        'views/account/register.xml',

        # Customer account portal
        'views/account/dashboard.xml',
        'views/account/orders.xml',
        'views/account/addresses.xml',
        'views/account/payment_methods.xml',
        'views/account/account_details.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # Core styles
            'custom_shop_templates/static/src/scss/variables.scss',
            'custom_shop_templates/static/src/scss/_base.scss',
            'custom_shop_templates/static/src/scss/_utilities.scss',
            'custom_shop_templates/static/src/scss/components.scss',
            'custom_shop_templates/static/src/scss/components/_banners.scss',

            # Summary components (base → variants → specific)
            'custom_shop_templates/static/src/scss/components/_summary-base.scss',
            'custom_shop_templates/static/src/scss/components/_cart-summary.scss',
            'custom_shop_templates/static/src/scss/components/_checkout-summary.scss',

            # Page-specific styles
            'custom_shop_templates/static/src/scss/pages/_cart.scss',
            'custom_shop_templates/static/src/scss/pages/_checkout-address.scss',
            'custom_shop_templates/static/src/scss/pages/_checkout-shipping.scss',
            'custom_shop_templates/static/src/scss/pages/_checkout-payment.scss',
            'custom_shop_templates/static/src/scss/pages/_login.scss',
            'custom_shop_templates/static/src/scss/pages/_register.scss',
            'custom_shop_templates/static/src/scss/pages/_account-layout.scss',
            'custom_shop_templates/static/src/scss/pages/_account-navigation.scss',
            'custom_shop_templates/static/src/scss/pages/_dashboard.scss',
            'custom_shop_templates/static/src/scss/pages/_account-details.scss',
            'custom_shop_templates/static/src/scss/pages/_addresses.scss',
            'custom_shop_templates/static/src/scss/pages/_payment-methods.scss',
            'custom_shop_templates/static/src/scss/pages/_orders.scss',

            # JavaScript
            'custom_shop_templates/static/src/js/product_variant_autoselect.js',
            # 'custom_shop_templates/static/src/js/cart.js',  # TODO: File missing
            # Inline script in template instead
            # 'custom_shop_templates/static/src/js/checkout_address.js',
            'custom_shop_templates/static/src/js/addresses.js',
            'custom_shop_templates/static/src/js/payment-method-toggle.js',
            'custom_shop_templates/static/src/js/prefetch.js',
            'custom_shop_templates/static/src/js/account-selector.js',
        ],
    },
    'images': [
        # 'static/description/icon.png',  # Add module icon if needed
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}