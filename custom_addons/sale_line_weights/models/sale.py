# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    weights = fields.Text('Weights')
    total_weight = fields.Float('Total Weight')
    packs = fields.Integer('# Packs')

    @api.onchange('weights')
    def onchange_weights(self):
        weight=0
        if self.weights:
            weight_list = self.weights.split(',')
            weight_list = [weight for weight in weight_list if weight]
            print(weight_list,"wwwwwww")
            for elem in weight_list:
                weight += float(elem)
            self.total_weight = weight
            if weight > 0:
                self.product_uom_qty = weight
                self.packs = len(weight_list)

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        # res = super(SaleOrderLine,self)._prepare_invoice_line(quantity=qty)
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        if self.weights:
            res['weights'] = self.weights
            res['total_weight'] = self.total_weight
        res['packs'] = self.packs
        return res

