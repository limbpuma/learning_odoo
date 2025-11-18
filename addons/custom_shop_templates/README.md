# TTS Custom Shop Templates

Custom templates for Odoo e-commerce that replace the default look with something more professional and branded.

## What does it do?

This module gives your Odoo shop a custom design instead of using Odoo's default templates. It covers:
- Customer account pages (dashboard, orders, addresses)
- Login and registration pages
- Product pages and shopping cart
- Custom styling with your brand colors

## How complete is it?

**90% done with account portal**
The customer account section is mostly finished. Dashboard, orders, addresses, payment methods - all working. Just some polish left to do.

**Login/register pages are done**
Authentication is complete with custom styling.

**Shop pages are in progress**
Product listings, detail pages, and cart have basic implementations. Checkout flow is coming next once we finalize the design.

## What's included?

**Customer Account Area:**
- Dashboard with recent orders
- Order history
- Address management (billing & shipping)
- Payment preferences
- Account details editing

**Authentication:**
- Login page
- Registration with validation

**Shop:**
- Product catalog
- Product details with variants
- Shopping cart
- Related products

**Under the hood:**
- Built with Bootstrap 5
- Modular SCSS (easy to customize colors and spacing)
- Responsive design (works on phones, tablets, desktops)
- BentonSans font included
- Reusable components (buttons, cards, navigation)

## Quick setup

1. Drop this folder in your Odoo addons directory
2. Restart Odoo
3. Go to Apps → Update Apps List
4. Search for "TTS Custom Shop Templates"
5. Hit Install

## Testing it out

After installing, check these URLs:

**Account stuff:**
- `/my` - Dashboard
- `/my/orders` - Order history
- `/my/addresses` - Addresses
- `/my/payment_method` - Payment settings
- `/my/account` - Account details

**Login:**
- `/web/login` - Login page
- `/web/signup` - Register page

**Shopping:**
- `/shop` - Product catalog
- `/shop/cart` - Shopping cart

## File organization

```
custom_shop_templates/
├── controllers/      # Account page logic
├── models/          # Data models
├── views/
│   ├── account/     # Customer pages
│   ├── layout/      # Header, footer
│   ├── components/  # Reusable bits
│   └── shop/        # Product pages
└── static/
    ├── scss/        # Stylesheets (10 page-specific files)
    ├── js/          # JavaScript
    └── img/         # Icons
```

## Key details

**Requires:** Odoo 18.0+, plus the website, website_sale, and portal modules

**Brand colors:** Light peach (#FFEBDC), black (#000000), orange (#FF4600)

**Fonts:** BentonSans in three weights (regular, medium, bold)

**Breakpoints:** Mobile (<576px), Tablet (576-992px), Desktop (>992px)

## Things to know

**Desktop first:** Desktop layouts are solid. Mobile and tablet still need some work.

**CSS cleanup:** I'm gradually moving from inline styles to proper CSS classes. About 60% done with that migration.

**Naming:** All custom classes start with `tts-` to avoid conflicts with Odoo's own styles.

---
