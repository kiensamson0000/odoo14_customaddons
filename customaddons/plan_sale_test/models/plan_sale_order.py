from odoo import fields, models, api


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'

    sale_order_plan_sale = fields.One2many("sale.order", "plan_sale_sale_order")

    sender_name = fields.Char(string="Name", require=True)
    id_quotation = fields.Char(related="sale_order_plan_sale.name", readonly=True)
    information_plan = fields.Text(string="Information Business Plan", require=True)

    status = fields.Selection([('approved', "Approved"),
                               ('waiting_approved', "Waiting Approved"),
                               ('denied', "Denied")], default="waiting_approved")

    res_partner_form_approval = fields.Many2one("res.partner", string="Approval")




