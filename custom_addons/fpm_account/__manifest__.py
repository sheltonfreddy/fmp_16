# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'FPM Account Customisations',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 15,
    'summary': 'FPM Account Customisations',
    'depends': ['account', 'fmp_reports'],
    'data': [
        'report/invoice_report_templates.xml',
        'report/invoice_report.xml',
        'views/invoice_view.xml',
        'views/report.xml',
        'report/customer_invoices_due_report_template.xml',
        'report/product_packs_invoiced_report_template.xml',
        'wizard/partner_inv_report_view.xml',
        'wizard/product_packs_invoiced_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False
}
