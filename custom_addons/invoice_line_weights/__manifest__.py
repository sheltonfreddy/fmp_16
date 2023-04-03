# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Invoice Line Weights',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 15,
    'summary': 'Invoice Line Weight',
    'depends': ['account'],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
