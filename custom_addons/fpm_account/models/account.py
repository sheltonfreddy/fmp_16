from odoo import api, fields, models, _


# class AccountMove(models.Model):
#     _inherit = 'account.move'
#
#     def invoice_print_without_pay(self):
#         """ Print the invoice without payment
#         """
#         self.ensure_one()
#         return self.env.ref('account.account_invoices_without_payment').report_action(self)

    # @api.multi
    # def invoice_validate(self):
    #     for invoice in self.filtered(lambda invoice: invoice.partner_id not in invoice.message_partner_ids):
    #         invoice.message_subscribe([invoice.partner_id.id])
    #     for invoice in self:
    #         invoice.merge_lines()
    #     self._check_duplicate_supplier_reference()
    #     return self.write({'state': 'open'})

    # @api.one
    # def merge_lines(self):
    #     print ("ccccc")
    #     to_delete = []
    #     itered = []
    #     for line in self.invoice_line_ids:
    #         itered.append(line.id)
    #         line_to_merge = self.invoice_line_ids.search([('invoice_id', '=', self.id),
    #                                                   #('discount', '=', line.discount),
    #                                                   #('invoice_line_tax_id', '=', line.invoice_line_tax_id.id),
    #                                                   ('price_unit', '=', line.price_unit),
    #                                                   ('product_id', '=', line.product_id.id),
    #                                                   #('account_id', '=', line.account_id.id),
    #                                                  # ('account_analytic_id', '=', line.account_analytic_id.id),
    #                                                   ('id', 'not in', itered)], limit=1)
    #         if line_to_merge:
    #             to_delete.append(line.id)
    #             line_to_merge.write({'quantity': line_to_merge.quantity + line.quantity,
    #                                  'total_weight': line_to_merge.quantity + line.quantity,
    #                                  'packs': line_to_merge.packs + line.packs,
    #                                  'weights':line_to_merge.weights+','+line.weights if (
    #                                         line_to_merge.weights and line.weights) else False,
    #                                  'origin': line_to_merge.origin + line.origin if (
    #                                          line_to_merge.origin and line.origin) else False})
    #
    #     self.write({'invoice_line_ids': [(2, x, 0) for x in to_delete]})

