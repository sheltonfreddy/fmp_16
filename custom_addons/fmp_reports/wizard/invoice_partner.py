# -*- coding: utf-8 -*-

from odoo import api, fields, models


class InvoicePartner(models.TransientModel):
    _name = "invoice.partner.report"
    _rec_name = 'partner_id'
    partner_id = fields.Many2one('res.partner', string='Customer')
    inv_status = fields.Selection([
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('open_paid', 'Open & Paid'),
    ], string='Invoice Status', default='open', required=True)
    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)

    def print_report(self):
        data = {'form': self.read(['date_from', 'date_to', 'partner_id', 'inv_status'])[0]}
        return self.env.ref('fmp_reports.action_report_partner_invoice').report_action(self, data=data, config=False)
