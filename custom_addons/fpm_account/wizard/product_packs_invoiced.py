from datetime import date
from odoo import api, fields, models


class ProductPacksWizard(models.TransientModel):
    _name = 'product.packs.wizard'
    _description = 'Product Packs Wizard'

    product_ids = fields.Many2many('product.product', string='Products')
    date = fields.Date('Date')

    def action_generate_report(self):
        # Add your report generation logic here.
        product_ids = self.product_ids.ids
        data = {
            'product_ids': product_ids,
            'date': self.date,
        }
        print(data,"DDDDDDDDDD")
        return self.env.ref('fpm_account.product_packs_invoiced_report').report_action(self, data=data)

    # def action_generate_report(self):
    #     # Prepare data for the report
    #     product_ids = self.product_ids.ids
    #     data = {
    #         'product_ids': product_ids,
    #         'date': self.date,
    #     }
    #     return {
    #         'type': 'ir.actions.report',
    #         'report_name': 'fpm_account.product_packs_invoiced_report',
    #         'report_type': 'qweb-pdf',
    #         'data': {'data': data},
    #         'context': {'active_model': self._name, 'active_ids': self.ids},
    #     }
