# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'FPM Sales Customisations',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 15,
    'summary': 'FPM Sales Customisations',
    'depends': ['sale','barcodes'],
    'data': [

       # 'report/sale_report_templates.xml',
        'report/sale_report.xml',
        'views/sale_view.xml',
        'views/assets.xml',

    ],
    'installable': True,
    'auto_install': False
}
