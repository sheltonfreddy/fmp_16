# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'FPM Account Customisations',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 15,
    'summary': 'FPM Account Customisations',
    'depends': ['account'],
    'data': [
        'report/invoice_report_templates.xml',
        'report/invoice_report.xml',
        # 'views/invoice_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
