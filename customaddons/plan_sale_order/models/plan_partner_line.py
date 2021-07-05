from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError


class PlanPartnerLine(models.Model):
    _name = "plan.partner.line"

    def check_approve(self):
        self.status = 'approved'
        message = _(
            "%(partner_name)s approved the plan %(plan_name)s.",
            partner_name=self.partner.display_name,
            plan_name=self.plan_id.name
        )
        self.plan_id.message_post(body=message, subject='Plan Approving',
                                  partner_ids=self.plan_id.create_uid.partner_id.ids)

    def check_refuse(self):
        self.status = 'refused'
        message = _(
            "%(partner_name)s refused the plan %(plan_name)s.",
            partner_name=self.partner.display_name,
            plan_name=self.plan_id.name,
        )
        self.plan_id.message_post(body=message, subject='Plan Refusing',
                                  partner_ids=self.plan_id.create_uid.partner_id.ids)

    def _check_current_user(self):
        for rec in self:
            if rec.env.user.partner_id.id == rec.partner.id:
                rec.is_current_user = True
            else:
                rec.is_current_user = False

    plan_id = fields.Many2one('plan.sale.order', string='Sale Plan', ondelete='cascade')
    partner = fields.Many2one('res.partner', string='Approver')
    status = fields.Selection(string='Status', selection=[
        ('pending', 'Waiting for Approvement'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], required=True, default='pending')
    is_current_user = fields.Boolean(default=False, compute='_check_current_user')
