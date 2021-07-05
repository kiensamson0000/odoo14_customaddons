from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #add field new
    plan = fields.Many2one('plan.sale.order', string='Sale Plan')

    # ham get plan
    def _get_plan(self):
        plan = self.env['plan.sale.order'].search([('id', '=', id)], limit=1)
        if plan:
            self.plan = plan

    #ham kiem tra sale plan
    def action_confirm(self):
        # chưa có/ chưa duyệt -> error
        if self.plan.state != 'approved':
            raise ValidationError(_(
                'This quotation can not be confirmed because the sale plan %(plan)s has not been approved.',
                plan=self.plan.name
            ))
        else:
            # xác nhận thành công
            if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                raise UserError(_(
                    'It is not allowed to confirm an order in the following states: %s'
                ) % (', '.join(self._get_forbidden_state_confirm())))

            for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                order.message_subscribe([order.partner_id.id])
            self.write(self._prepare_confirmation_values())

            # Context key 'default_name' is sometimes propagated up to here.
            # We don't need it and it creates issues in the creation of linked records.
            context = self._context.copy()
            context.pop('default_name', None)

            self.with_context(context)._action_confirm()
            if self.env.user.has_group('sale.group_auto_done_setting'):
                self.action_done()
            return True
