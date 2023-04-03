# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'FMP Reports',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 15,
    'summary': 'FMP Reports',
    'depends': ['account', 'accounting_pdf_reports'],
    'data': [
        'views/report_invoice_partner_view.xml',
        'wizard/invoice_partner_wiz_view.xml',
        'views/invoice_partner.xml',


    ],
    'installable': True,
    'auto_install': False
}
