from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"
    _description = "setting debt limit"

    money_debt = fields.Float(string='Hạn mức tiền nợ')
    time_debt = fields.Float(string='Hạn mức thời gian nợ (Tháng)')

    def check_debt_customer(self):
        money_debit = 0
        for order in self.sale_order_ids:
            if order.state == 'sale':
                money_debit += order.amount_total

        for invoice_line in self.invoice_ids:
            if invoice_line.move_type == 'out_invoice':
                if invoice_line.payment_state in ('in_payment', 'partial', 'paid'):
                    money_debit += - invoice_line.amount_total + invoice_line.amount_residual
                else:
                    pass
            # Xu ly truong hop hoan tra
            # 2 case: hoan tra khi da thanh toan & hoan tra chua thanh_toan/thanh_toan 1 phan
            #
            # elif invoice_line.move_type == 'out_refund':
            #     if invoice_line.payment_state in ('partial', 'in_payment', 'paid'):
                      # Da xu ly truong hop neu thanh toan đủ
            #         # test = invoice_line.amount_residual
            #         # money_debit = money_debit - invoice_line.amount_residual
            #
            #         # Chua xu ly hoan tra chua thanh_toan/thanh_toan 1 phan
            #         if invoice_line.move_type == 'out_invoice' and invoice_line.payment_state == 'reversed':
            #             money_debit += - invoice_line.amount_total
            #         else:
            #             money_debit = money_debit - invoice_line.amount_residual
            #         # invoice_payments_widget
            #     else:
            #         pass
            else:
                pass
        print(money_debit)
        return money_debit
