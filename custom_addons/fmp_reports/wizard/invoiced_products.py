# -*- coding: utf-8 -*-

from odoo import api, fields, models


class InvoicedProducts(models.TransientModel):
    _name = "invoiced.products"
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    display_quantity = fields.Boolean(string='Display Quantity', default=True)
    product_ids = fields.Many2many('product.product', string='Products')

    def print_report(self):
        data = {'form': self.read(['from_date', 'to_date', 'display_quantity', 'product_ids'])[0]}
        return self.env.ref('fmp_reports.action_report_invoiced_products').report_action(self, data=data, config=False)
