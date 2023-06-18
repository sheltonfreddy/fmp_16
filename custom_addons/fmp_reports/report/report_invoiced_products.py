# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools
from odoo.exceptions import UserError
from decimal import Decimal, ROUND_HALF_UP



class InvoicedProductsReport(models.Model):
    _name = 'report.fmp_reports.report_invoiced_products'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        model = self.env.context.get('active_model')
        domain = [
            ('date', '>=', data['form']['from_date']),
            ('date', '<=', data['form']['to_date']),
            ('product_id', 'in', data['form']['product_ids']),
            ('move_id.state', '=', 'posted'),
            ('move_id.move_type', 'in', ('out_invoice', 'out_refund'))  # to consider only customer invoices and credit notes
        ]
        invoice_line_ids = self.env['account.move.line'].search(domain)
        report_data = {}
        for line in invoice_line_ids:
            product = line.product_id
            quantity = Decimal(line.quantity).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            if product not in report_data:
                report_data[product] = {'packs': line.packs, 'quantity': quantity}
            else:
                report_data[product]['packs'] += line.packs
                report_data[product]['quantity'] += quantity

        for product in report_data:
            report_data[product]['quantity'] = float(report_data[product]['quantity'])

        sorted_report_data = dict(sorted(report_data.items(), key=lambda item: item[1]['quantity'], reverse=True))
        return {
            'doc_model': model,
            'data': data,
            'report_data': sorted_report_data

        }
