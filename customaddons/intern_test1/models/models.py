from odoo import fields, models, api
import re


class SaleOder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Inherit'

    discount_estimated = fields.Monetary(string='Estimated Discount Total', readonly=True, store=True,   # Monetary field support values tiền tệ  ; readonly=True thì field chỉ đọc, ko sửa or stored, store=True sau khi tính toán, các trường đc stored trong CSDL, đc truy xuất giống như fields thay vì tính toán lại
                                         compute='estimate_discount_total')    # compute link đến def ...
    customer_discount_code = fields.Text(string="Customer Discount Code", related='partner_id.customer_discount_code')  # relate: ref đến field customer_discount_code qua field partner_id  (khách hàng)
    valid_code = fields.Boolean(string='Valid Code', store=True, related='partner_id.valid_code', readonly=True)  # related: ref đến field code_coupon_ customer qua field partner_id  (khách hàng)

    @api.depends('amount_total', 'partner_id', 'customer_discount_code')
    def estimate_discount_total(self):
        for rec in self:
            if rec.valid_code:
                discount_code = self.customer_discount_code.split('_')
                discount_vals = int(discount_code[1])
                rec.discount_estimated = rec.amount_total * (100 - discount_vals) / 100
            else:
                rec.discount_estimated = rec.amount_total


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner Inherit'

    customer_discount_code = fields.Text(string="Customer Code")
    valid_code = fields.Boolean(string='Valid Code', compute='check_valid', store=True)

    @api.depends('customer_discount_code')
    def check_valid(self):
        for rec in self:
            if not rec.customer_discount_code:
                rec.valid_code = False
            else:
                if re.match("^VIP_([1-9]|[1-9][0-9]|0[1-9])$", rec.customer_discount_code):
                    rec.valid_code = True
                else:
                    rec.valid_code = False

