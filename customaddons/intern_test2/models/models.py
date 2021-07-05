# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
# from dateutil import relativedelta
from dateutil.relativedelta import relativedelta

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product Inherit'

    product_warranty = fields.Text(string="Product Warranty Code", readonly=True, compute='create_product_warranty')
    date_to = fields.Date(string='Date To')
    date_from = fields.Date(string='Date From')
    time_interval = fields.Text(string="Time Interval", compute='check_date_stop_warranty')
    check_valid_date = fields.Boolean(string='Check Valid')

    @api.depends('date_to', 'date_from')
    def create_product_warranty(self):
        for rec in self:
            date_to = rec.date_to
            date_from = rec.date_from
            if date_from and date_to:
                date_to = date_to.strftime('%d%m%-y')
                date_from = date_from.strftime('%d%m%-y')
                rec.product_warranty = 'PWR/' + str(date_from) + '/' + str(date_to)
                rec.check_valid_date = True
            else:
                rec.check_valid_date = False
                rec.product_warranty = ''

    @api.constrains('date_to', 'date_from')        #kiểm tra rằng buộc
    def check_date(self):
        for rec in self:
            if rec.date_from and rec.date_to:       # thử sửa 2 dòng ì thành 1, <
                if rec.date_to < rec.date_from:
                    raise ValidationError('Date Start Warranty is smaller than Date Stop Warranty.')

    @api.depends('date_to')
    def check_date_stop_warranty(self):
        current_date = datetime.today().date()
        for rec in self:
            date_to = rec.date_to
            count_days = ''
            if rec.date_to:
                if current_date < rec.date_to:
                    date_to = datetime.strptime(str(date_to), "%Y-%m-%d").date()
                    rd = relativedelta(date_to, current_date)                   #relativedelta: kiểu tương đối, áp dụng ngày giờ hiện có, thay thế cụ thể = khoảng time
                    if rd.years == 0 and rd.months == 0:
                        count_days = str(rd.days) + "d"
                    elif rd.years == 0 and rd.months != 0:
                        count_days = str(rd.months) + "m" + " " + str(rd.days) + "d"
                    elif rd.years != 0 and rd.months == 0:
                        count_days = str(rd.years) + "y" + " " + str(rd.days) + "d"
                    else:
                        count_days = str(rd.years) + "y" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
            rec.time_interval = count_days


class SaleOder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Inherit'

    discount_with_warranty = fields.Monetary(string='Estimated Discount Total With Product Warranty', readonly=True,
                                             store=True, compute='discount_total_with_warranty')

    @api.depends('order_line')
    def discount_total_with_warranty(self):
        for rec in self:
            estimated_total = 0.0
            for line in rec.order_line:
                estimated_total += line.product_price
        rec.update({
            'discount_with_warranty': estimated_total
        })

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_price = fields.Monetary(string='Product Price', compute='calculate_price')

    @api.onchange('price_subtotal')
    def calculate_price(self):
        for order in self:
            if order.product_id:
                if not order.product_id.product_warranty:
                    order.product_price = order.price_subtotal * 0.9
                else:
                    order.product_price = order.price_subtotal