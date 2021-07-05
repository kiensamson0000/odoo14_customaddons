
from odoo import api, fields, models, tools,_
from odoo.exceptions import ValidationError, UserError



from odoo import api, fields, models, tools,_

class UpdateCustomerCode(models.TransientModel):
    _name = 'update.customer.code'
    _description = 'Update Customer Code'

    customer_discount_code = fields.Text(string="Customer Code")

    def update(self):
        ids = self.env.context['active_ids']  # selected record ids
        list = self.env['res.partner'].browse(ids)
        for rec in list:
            rec.customer_discount_code = self.customer_discount_code

#
# import logging
# _logger = logging.getLogger(__name__)
#
# class UpdateCouponsCode(models.TransientModel):
#     _name = "update.coupons.code"
#     _description = "Update coupons code"
#
#     customer_discount_code = fields.Text(string="Discount Code")
#
#     def updatecoupon(self):
#         list = self.env['res.partner'].browse(self._context['active_ids'])
#
#         for rec in list:
#             rec.customer_discount_code = self.customer_discount_code
#
#         # # cach khac
#         # ids = self.env.context['active_ids']
#         # customize_coupons =  self.env["res.partner"].browser(ids)
#         # new_data={}
#         # if self.customer_discount_code:
#         #     new_data["customer_discount_code"] = self.customer_discount_code
#         #
#         # customize_coupons(new_data)
