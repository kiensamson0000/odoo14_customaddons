from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # inherit use to Messaging features


    name = fields.Text(string='Name', required=True, tracking=True) #tracking = thông báo field name khi sửa
    quotation = fields.Many2one('sale.order', string='Quotation', readonly=True, ondelete='cascade') #ondelete='cascade' xóa cha -> mất cả con
    detail = fields.Text(string='Detail information about plan', required=True, tracking=True)
    sent = fields.Boolean(string='Sent or not', default=False)
    edited = fields.Boolean(string='Edited or not', default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], string='Status', readonly=True, default='draft', compute='_check_status', tracking=True)
    partner_lines = fields.One2many('plan.partner.line', 'plan_id', tracking=True)  #inverse_name ('plan_id'): Điều này chỉ áp dụng cho One2many và là tên trường trong mô hình đích cho quan hệ Many2one ngược.
    # check_sale_plan = fields.Boolean(string='Check Sale PLan')


    # hàm send plan với message: created, edited
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
        self.message_post(body=message, subject='Plan to you',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          partner_ids=self.partner_lines.partner.ids)

    # hàm check status cho cả người create sale plan và approver
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

    # @api.depends('name')
    # def check_sale_order_plan(self):
    #     for rec in self:
    #         name = rec.name
    #         if name:
    #             rec.check_sale_plan = True
    #         else:
    #             rec.check_sale_plan = False

