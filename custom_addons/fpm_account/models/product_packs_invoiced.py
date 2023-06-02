from odoo import models, fields, api
from collections import defaultdict
from datetime import datetime



class ProductsWithPacksInvoiced(models.AbstractModel):
    _name = 'report.fpm_account.product_packs_report_template'

    # @api.model
    # def _get_report_values(self, data=None):
    #     if data is None:
    #         data = {}
    #     product_ids = data.get('product_ids', [])
    #     print("ppppp000000", product_ids, type(product_ids))
    #     if isinstance(product_ids, str):
    #         product_ids = json.loads(product_ids)
    #     date = data.get('date', None)
    #     products = self.env['product.product'].browse(product_ids)
    #     print(products, "ppppppppp")
    #     report_data = []
    #
    #     for product in products:
    #         packs_invoiced = self.env['account.move.line'].search([
    #             ('product_id', '=', product.id),
    #             ('date', '=', date),
    #         ]).mapped('packs')
    #
    #         total_packs_invoiced = sum(packs_invoiced)
    #
    #         report_data.append({
    #             'product': product.name,
    #             'packs_invoiced': total_packs_invoiced,
    #             # "doc_ids": docids,
    #         })
    #
    #     return report_data

    @api.model
    def _get_report_values(self, docids, data=None):
        print("Starting _get_report_values method...")  # Added print statement at the start

        if data is None:
            data = {}
        product_ids = data.get('product_ids', [])
        selected_date = data.get('date', None)
        print(product_ids,selected_date,"000000000000" )
        products = self.env['product.product'].browse(product_ids)
        report_data = []

        for product in products:
            packs_invoiced = self.env['account.move.line'].search([
                ('product_id', '=', product.id),
                ('date', '=', selected_date),
            ]).mapped('packs')

            total_packs_invoiced = sum(packs_invoiced)

            report_data.append({
                'product': product.name,
                'packs_invoiced': total_packs_invoiced,
            })
        print(report_data,"ddddddd")
        customer_data = []
        customer_ids = self.env['account.move'].search([
            ('invoice_date', '=', selected_date),
            ('move_type', 'in', ['out_invoice', 'out_refund'])
        ]).mapped('partner_id')
        for customer in customer_ids:
            for product in products:
                move_lines = self.env['account.move.line'].search([
                    ('move_id.invoice_date', '=', selected_date),
                    ('move_id.partner_id', '=', customer.id),
                    ('move_id.move_type', 'in', ['out_invoice', 'out_refund']),
                    ('product_id', '=', product.id),
                ])

                total_packs_invoiced = sum(move_lines.mapped('packs'))
                if total_packs_invoiced > 0:
                    customer_data.append({
                        'customer': customer.name,
                        'product': product.name,
                        'packs_invoiced': total_packs_invoiced,
                    })
        # Prepare the structure for customer_data
        # customer_data1 = defaultdict(list)
        #
        # # Iterate over the customers
        # for customer in customer_ids:
        #     # Query invoices for the current customer
        #     invoices = self.env['account.move'].search([
        #         ('partner_id', '=', customer.id),
        #         ('invoice_date', '=', selected_date),
        #         ('move_type', '=', 'out_invoice'),
        #     ])
        #
        #     # Iterate over the invoice lines of the invoices
        #     for invoice in invoices:
        #         for line in invoice.invoice_line_ids:
        #             if line.product_id.id in product_ids:
        #                 packs_invoiced = line.packs
        #
        #                 if packs_invoiced > 0:
        #                     # Append data to the corresponding product in the structure
        #                     customer_data1[line.product_id.name].append({
        #                         'customer': customer.name,
        #                         'packs_invoiced': packs_invoiced,
        #                     })
        #
        # # Convert defaultdict back to dict for compatibility
        # customer_data1 = dict(customer_data1)
        # print(customer_data1,"ccccccc")
        # print("Ending _get_report_values method...")  # Added print statement at the end

        # We still use defaultdict, but now it will default to a dict
        customer_data1 = defaultdict(lambda: defaultdict(int))

        # Iterate over the customers
        for customer in customer_ids:
            # Query invoices for the current customer
            invoices = self.env['account.move'].search([
                ('partner_id', '=', customer.id),
                ('invoice_date', '=', selected_date),
                ('move_type', '=', 'out_invoice'),
            ])

            # Iterate over the invoice lines of the invoices
            for invoice in invoices:
                for line in invoice.invoice_line_ids:
                    if line.product_id.id in product_ids:
                        packs_invoiced = line.packs

                        if packs_invoiced > 0:
                            # Add packs_invoiced to the existing value in the structure
                            customer_data1[line.product_id.name][customer.name] += packs_invoiced

        # Convert defaultdict back to dict for compatibility
        customer_data1 = {k: dict(v) for k, v in customer_data1.items()}

        return {
            'doc_ids': docids,
            'doc_model': 'account.move.line',
            #'docs': self.env['account.move.line'].browse(docids),
            'report_data': report_data,
            'customer_data': customer_data,
            'customer_data1': customer_data1,
            'date': datetime.strptime(selected_date, "%Y-%m-%d")

        }
