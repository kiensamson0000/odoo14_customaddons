from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def send_plan(self):
        self.sent = True
        if self.edited == False:
            message = _(
                "Plan %(name)s for quotation %(quotation)s was created",
                name=self.name,
                quotation=self.quotation.name
            )
        else:
            message = _(
                "Plan %(name)s for quotation %(quotation)s was edited.",
                name=self.name,
                quotation=self.quotation.name
            )
        self.message_post(body=message, subject='Plan to you', partner_ids=self.partner_lines.partner.ids)

    def _check_status(self):
        partner_num = len(self.partner_lines)
        approve_num = 0
        refuse_num = 0
        for partner in self.partner_lines:
            if partner.status == 'approved':
                approve_num += 1
            if partner.status == 'refused':
                refuse_num += 1
        if approve_num == partner_num and partner_num != 0:
            self.state = 'approved'
        elif refuse_num != 0:
            self.state = 'refused'
        else:
            if self.sent == True:
                self.state = 'sent'
            else:
                self.state = 'draft'

    @api.onchange('name', 'detail', 'partner_lines')
    def _change_state_when_edited(self):
        self.state = 'draft'
        self.sent = False
        self.edited = True

    name = fields.Text(string='Name', required=True, tracking=True)
    quotation = fields.Many2one('sale.order', string='Quotation', readonly=True, ondelete='cascade')
    detail = fields.Text(string='Detail information about plan', required=True, tracking=True)
    sent = fields.Boolean(string='Sent or not', default=False)
    edited = fields.Boolean(string='Edited or not', default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], string='Status', readonly=True, default='draft', compute='_check_status', tracking=True)
    partner_lines = fields.One2many('plan.partner.line', 'plan_id', tracking=True)
