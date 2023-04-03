# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    # def _add_product(self, product, weight, qty=1.0):
    #     # order_line = self.order_line.filtered(lambda r: r.product_id.id == product.id and
    #     #                                                 (r.weights and r.weights.split(',') and
    #     #                                                  len(r.weights.split(',')) < 5))
    #     # order_line = self.order_line.sorted(key=lambda r: r.id).filtered(lambda r: r.product_id.id == product.id and
    #     #                                                                            (r.weights and r.weights.split(
    #     #                                                                                ',') and
    #     #                                                                             len(r.weights.split(',')) < 5))[0]
    #     order_line = self.order_line.sorted(key=lambda r: r.create_date).filtered(
    #         lambda r: r.product_id.id == product.id and
    #                   (r.weights and r.weights.split(',') and
    #                    len(r.weights.split(',')) < 5))
    #
    #     if order_line and order_line.weights and order_line.weights.split(',') and \
    #             len(order_line.weights.split(',')) < 5:
    #         order_line.weights += ',' + weight
    #         order_line.onchange_weights()
    #     else:
    #         vals = {
    #             'product_id': product.id,
    #             'product_uom': product.uom_id.id,
    #             'state': 'draft',
    #             'weights': weight
    #             }
    #         line = self.order_line.new(vals)
    #         line.onchange_weights()
    #         self.order_line += line

    # def on_barcode_scanned(self, barcode):
    #     if barcode:
    #         barcode_weight = barcode.split()
    #         print("barcode_weight","BBBBBBBBBBBB")
    #         if len(barcode_weight) != 2:
    #             raise UserError(_('Product code and Weight not Captured! Please try again!!'))
    #     if self.state != 'draft':
    #         return
    #     product = self.env['product.product'].search([('barcode', '=', barcode_weight[0])])
    #     if product and weight:
    #         weight = barcode_weight[1]
    #         self._add_product(product, weight)

    def _add_product(self, product, weight, qty=1.0):
        order_line = self.order_line.filtered(lambda r: r.product_id.id == product.id and
                                                        (r.weights and r.weights.split(',') and
                                                         len(r.weights.split(',')) < 5))
        if order_line:
            for line in order_line:
                if line.weights and line.weights.split(',') and len(line.weights.split(',')) < 5:
                    line.weights += ',' + weight
                    line.onchange_weights()
                    break
            else:
                vals = {
                    'product_id': product.id,
                    'product_uom': product.uom_id.id,
                    'state': 'draft',
                    'weights': weight
                }
                line = self.order_line.new(vals)
                line.onchange_weights()
                self.order_line += line
        else:
            vals = {
                'product_id': product.id,
                'product_uom': product.uom_id.id,
                'state': 'draft',
                'weights': weight
            }
            line = self.order_line.new(vals)
            line.onchange_weights()
            self.order_line += line

    def on_barcode_scanned(self, barcode):
        if self.state != 'draft':
            return
        if barcode:
            barcode_weight = barcode.split()
            if len(barcode_weight) != 2:
                raise UserError(_('Product code and Weight not Captured! Please try again!!'))
            product = self.env['product.product'].search([('barcode', '=', barcode_weight[0])])
            if not product:
                raise UserError(_('Product not found!'))
            weight = barcode_weight[1]
            self._add_product(product, weight)
        else:
            raise UserError(_('Barcode not detected!'))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    last_price = fields.Float('Last Price', compute="_compute_last_price", store=True)

    @api.depends('product_id', 'order_partner_id')
    def _compute_last_price(self):
        """ Compute last price
        """
        for line in self:
            lines = self.env['sale.order.line'].search([('order_partner_id', '=', line.order_partner_id.id),
                                                        ('product_id', '=', line.product_id.id),
                                                        ('order_id', '!=', line.order_id.id),
                                                        ('order_id.state', 'not in', ['draft', 'cancel'])],
                                                       order='create_date DESC', limit=1)
            print(lines, "lllllllllllll")
            if not lines:
                line.last_price = 0
                break
            line.last_price = lines and lines.price_unit or 0

