
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import re


class CustomizeCoupons(models.Model):
    _inherit = "sale.order"  # <- inherit fields and methods from model "sale.order",
    _description = "Extend sales model"

    # add new field:
    customer_discount_code = fields.Text(string="Customer Discount Code", related='partner_id.customer_discount_code')  # relate: ref đến field code_coupon_ customer qua field partner_id  (khách hàng)
    sale_order_discount_estimated = fields.Monetary(string="Total Discount Estimated", readonly=True, store=True,
                                                    compute='toal_discount_estimated')
    valide_code = fields.Boolean(string="Valide code", readonly=True, store=True, related="partner_id.valide_code")

    @api.depends('amount_total', 'partner_id', 'customer_discount_code')
    def toal_discount_estimated(self):
        for rec in self:
            if rec.valide_code:
                discount_code = self.customer_discount_code.split('_')
                discount_vals = int(discount_code[1])
                rec.sale_order_discount_estimated = rec.amount_total * (100 - discount_vals) / 100
            else:
                rec.sale_order_discount_estimated = rec.amount_total

class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Res partner inherit"

    customer_discount_code = fields.Text(string="Customer Code")
    valide_code = fields.Boolean(string="Valide code", compute="check_discount_code", store=True)

    @api.depends('customer_discount_code')
    def check_discount_code(self):
        for rec in self:
            if not rec.customer_discount_code:
                rec.valide_code = False
            else:
                if re.match("^VIP_([1-9]|[1-9][0-9]|0[1-9])$", rec.customer_discount_code):
                    rec.valide_code = True
                else:
                    rec.valide_code = False

