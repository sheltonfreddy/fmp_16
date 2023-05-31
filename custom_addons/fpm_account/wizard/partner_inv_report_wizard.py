from odoo import models, fields, api


class CustomerInvoicesDueWizard(models.TransientModel):
    _name = 'customer.invoices.due.wizard'
    _description = 'Invoice Report'

    # Add your wizard fields here, e.g.:
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')

    def action_generate_report(self):
        # Add your report generation logic here.
        data = {
            'partner_id': self.partner_id.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('fpm_account.customer_invoices_due_report').report_action(self, data=data)
