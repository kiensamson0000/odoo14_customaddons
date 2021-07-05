from odoo import api, fields, models, tools,_

class UpdateCustomerCode(models.TransientModel):
    _name = 'update.customer.code'
    _description = 'Mass Update Customer Code'

    customer_discount_code = fields.Text(string="Customer Code")

    def update(self):
        list = self.env['res.partner'].browse(self._context['active_ids'])

        for rec in list:
            rec.customer_discount_code = self.customer_discount_code
