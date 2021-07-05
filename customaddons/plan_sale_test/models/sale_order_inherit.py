from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'


    plan_sale_sale_order = fields.Many2one("plan.sale.order")

    sender_name = fields.Char(string="Name")
    information_plan = fields.Text(string="Information Business Plan")

    status = fields.Selection(related="plan_sale_sale_order.status")

    def action_create_plan_sale(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Company',
            'view_mode': 'form',
            'res_model': 'create.plan.sale.wizard',
            'target': 'new',
            'context': {
                'default_id_quotation': self.id,
                'default_res_partner_ids': self.ids,
            }
        }
