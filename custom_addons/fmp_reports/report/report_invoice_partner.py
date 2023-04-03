# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class PartnerInvoiceReport(models.Model):
    _name = 'report.fmp_reports.report_invoice_partner'

    @api.model
    def get_report_values(self, docids, data=None):
        if not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        model = self.env.context.get('active_model')
        # docs = self.env[model].browse(self.env.context.get('active_id'))
        inv_status = data['form']['inv_status']

        domain = [('type', '=', 'out_invoice'),('date_invoice', '>=', data['form']['date_from']),
                  ('date_invoice', '<=', data['form']['date_to'])]
        if inv_status == 'open':
            domain.append(('state', '=', 'open'))
        elif inv_status == 'paid':
            domain.append(('state', '=', 'paid'))
        else:
            domain.append(('state', 'in', ['open', 'paid']))
        if data['form']['partner_id']:
            domain.append(('partner_id', '=', data['form']['partner_id'][0]))
        invoice_ids = self.env['account.move'].search(domain, order="date_invoice desc")
        # payment_ids = self.env['account.payment'].search(pay_domain, order="date_invoice desc")
        inv_data = []
        amount_total = 0
        for inv in invoice_ids:

            lines= {'partner_id': inv.partner_id.name, 'date_invoice': inv.date_invoice, 'invoice_number': inv.number,
                    'state': inv.state, 'amount_total': inv.amount_total}
            amount_total+=inv.amount_total
            inv_data.append(lines)
        data.update({'total_amt': amount_total})
        return {
            # 'doc_ids': docids,
            'doc_model': model,
            'invoices': inv_data,
            'data': data,

        }
