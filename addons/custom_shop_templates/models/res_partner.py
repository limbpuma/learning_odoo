# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    preferred_payment_method_code = fields.Selection([
        ('credit_card', 'Credit Card'),
        ('card', 'Credit Card (Legacy)'),  # Backward compatibility
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('demo', 'Demo'),
    ], string='Preferred Payment Method', help='The preferred payment method for this customer')
