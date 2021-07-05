from odoo import api, models, fields, _

from odoo.exceptions import UserError, ValidationError


class CreatePlan(models.TransientModel):
    _name = "create.plan"

    name = fields.Text(string='Name', required=True)
    detail = fields.Text(string='Detail information about plan', required=True)
    partner_lines = fields.Many2many('res.partner')


    def create_plan(self):
        quotation_id = self.env.context.get('active_ids', [])
        print(self.partner_lines)
        quotation = self.env['sale.order'].browse(quotation_id[0])
        vals = {
            'name': self.name,
            'quotation': quotation_id[0],
            'detail': self.detail,
            'state': 'new'
        }
        self.env['plan.sale.order'].create(vals)
        plan_id = self.env['plan.sale.order'].search([('quotation', '=', quotation_id[0])], limit=1).id
        quotation.write({'plan':plan_id})
        for partner in self.partner_lines:
            self.env['plan.partner.line'].create({
                'plan_id': plan_id,
                'partner': partner.id
            })

        message = _(
            "Plan for quotation %(quotation)s created successfully",
            quotation=quotation.name
        )
        quotation.message_post(body=message, subject='Sale Plan Creation')