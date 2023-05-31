from odoo import models, fields, api

class CustomerDueInvoicesReport(models.AbstractModel):
    _name = 'report.fpm_account.customer_invoices_due_report_template'
    _description = 'Customer Invoices Due Report'

    def _get_report_values(self, docids, data=None):
        if data is None:
            data = {}
        partner_id = data.get("partner_id", [None])
        date_from = data.get("date_from")
        date_to = data.get("date_to")

        query = """
                    SELECT m.name, m.date, p.display_name, m.invoice_date, m.amount_total,
                           m.amount_residual as residual_amount, m.move_type
                    FROM account_move m
                    LEFT JOIN res_partner p ON m.partner_id = p.id
                    WHERE m.partner_id = %s
                      AND m.state = 'posted'
                    ORDER BY m.invoice_date
                """
        #rint(query,"QQQQQ", partner_id, date_from, date_to)
        self.env.cr.execute(query, (partner_id,))
        report_lines = []
        running_total = 0.0
        total_balance_due = 0.0
        # for line in self.env.cr.dictfetchall():
        #     print (line,"llllll")
        #     if line['move_type'] == 'out_invoice':
        #         running_total += line['residual_amount']
        #         line['move_type'] = 'Invoice'
        #
        #     elif line['move_type'] == 'entry':
        #         running_total -= line['amount_total']
        #         line['move_type'] = 'Payment'
        #     line['running_total'] = running_total
        #     report_lines.append(line)
        #     total_balance_due = running_total
        # print(docids,data,report_lines,"9999999",total_balance_due)
        running_balance = 0.0
        report_lines = []
        for line in self.env.cr.dictfetchall():
            if line['move_type'] == 'out_invoice':
                running_balance += line['amount_total']
            elif line['move_type'] == 'entry':  # If the line is a payment
                running_balance -= line['amount_total']
            line['balance'] = running_balance
            total_balance_due = running_balance
            report_lines.append(line)

        return {
            "doc_ids": docids,
            "doc_model": "account.move",
            "data": data,
            "lines": report_lines,
            "total_balance_due": total_balance_due,
        }

