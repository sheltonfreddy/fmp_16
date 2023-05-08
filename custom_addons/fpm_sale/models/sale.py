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
    #
    # def _add_product(self, product, weight, qty=1.0):
    #
    #     order_line = self.order_line.filtered(lambda r: r.product_id.id == product.id and
    #                                                     (r.weights and r.weights.split(',') and
    #                                                      len(r.weights.split(',')) < 5))
    #     print(order_line, "oooooooooooo")
    #     line_found = False
    #
    #     if order_line:
    #         for line in order_line:
    #             print("Checking line:", line.id, line.weights)
    #             if line.weights and line.weights.split(',') and len(line.weights.split(',')) < 5:
    #                 line.weights += ',' + str(weight)
    #                 line.onchange_weights()
    #                 line_found = True
    #                 print("Updated line:", line.id, line.weights)
    #                 break
    #
    #     if not line_found:
    #         vals = {
    #             'product_id': product.id,
    #             'product_uom': product.uom_id.id,
    #             'state': 'draft',
    #             'weights': str(weight)  # Initialize weights as a string
    #         }
    #         line = self.order_line.new(vals)
    #         line.onchange_weights()
    #         self.order_line += line
    #         print("Created new line:", line.id, line.weights)

    def _add_product(self, product, weight, qty=1.0):
        weight = float(weight)  # Convert weight to float before processing
        existing_line = False

        for line in self.order_line:
            line_weight = line.product_id.weight
            weights = line.x_studio_field_mu5dT.split(',')
            weights = [float(w) for w in weights]  # Convert all weights to float

            if line.product_id == product and float(line_weight) == weight and len(
                    weights) < 5:  # Compare float values and check if there are less than 5 weights
                existing_line = True
                line.product_uom_qty += 1
                weights.append(weight)
                line.x_studio_field_mu5dT = ','.join([str(float(w)) for w in weights])  # Store weights as strings
                break

        if not existing_line:
            new_line = self.order_line.new({
                'product_id': product.id,
                'product_uom_qty': 1,
                'product_uom': product.uom_id.id,
                'price_unit': product.list_price,
                'x_studio_field_mu5dT': str(weight),  # Store weight as a string
                'name': product.name,
            })
            self.order_line += new_line

    def on_barcode_scanned(self, barcode):
        if self.state != 'draft':
            return
        print(barcode, "BBBBBBBBB", len(barcode))
        if barcode:
            if len(barcode) > 20:
                product_code = barcode[:16]  # extract the first 16 digits as the product code
                weight_index = barcode.find('3201')  # find the index of the '3201' pattern
                if weight_index == -1:  # if the pattern is not found, try the '3202' pattern
                    weight_index = barcode.find('3202')
                if weight_index == -1:  # if the pattern is still not found, raise an error
                    raise UserError(_('Weight information not found in the barcode!'))
                weight_string = barcode[weight_index + 4: weight_index + 10]
                weight_scale = 1 if barcode[weight_index: weight_index + 4] == '3201' else 100

                # Revised weight calculation
                weight = float(weight_string[:-1] + '.' + weight_string[-1]) / weight_scale

                weight_formatted = '{:.3f}'.format(weight)  # format the weight with 3 decimal places
                print("www22222", weight_formatted, float(weight_formatted))
                product = self.env['product.product'].search([('barcode', '=', product_code)])
                print(product_code, "<<<weight>>>", weight_formatted)
                if not product:
                    raise UserError(_('Product not found!'))
                self._add_product(product, weight_formatted)  # pass the formatted weight as float
            else:
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

