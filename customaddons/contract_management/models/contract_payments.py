from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import *

class ContractPayments(models.Model):
    _name = "contract.payments"
    _description = "Contract Payments"

    percent_payment = fields.Float(string='Percent Payments (%)')
    total_amount = fields.Float(compute='_compute_calculate_money')
    date_payment = fields.Date(default=date.today())

    contract_payment_customer = fields.Many2one('contract.management', string="Appointment")

    @api.depends('percent_payment')
    def _compute_calculate_money(self):
        check_percent = 0
        for rec in self:
            if not rec.percent_payment in range(0,100):
                raise ValidationError('Percent Payment Value must (0,100)')
            else:
                ### check dieu kien trong def check_onchange_payments_contract_id(self)
                rec.total_amount = rec.percent_payment / 100 * self.contract_payment_customer.amount_total

                ###
                # check_percent += rec.percent_payment
                # if check_percent <= 100:
                #     rec.total_amount = rec.percent_payment / 100 * self.contract_payment_customer.amount_total
                # else:
                #     raise ValidationError('Total Percent Payment Value must be equal to 100')
