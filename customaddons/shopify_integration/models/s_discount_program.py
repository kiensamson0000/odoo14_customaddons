# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools


class ShopifyDiscountProgram(models.Model):
    _name = "s.discount.program"
    _description = "Discount Program"

    name = fields.Char(string='Name')
    shop_id = fields.Many2one('s.shop', string='Shop ID')

    customer_ids = fields.One2many('s.discount.program.customer', 'discount_id', string='Discount Customer ID')
    product_ids = fields.One2many('s.discount.program.product', 'discount_id', string='Discount Product ID')

    @api.depends('shop_id')
    def get_customer(self):
        for rec in self:
            if rec.shop_id:
                # rec.customer_ids = rec.env['res.partner'].search([('shop_id', '=', rec.shop_id.id),
                #                                                   ('company_type', '=', 'person')], limit=50)
                rec.customer_ids = rec.env['res.partner'].search([('shop_id', '=', rec.shop_id.id)], limit=50)
            else:
                rec.customer_ids = rec.env['res.partner'].search([(0, '=', 1)])

    @api.onchange(shop_id)
    def get_product(self):
        for rec in self:
            if rec.shop_id:
                rec.product_ids = rec.env['product.template'].search([('shop_id', '=', rec.shop_id.id)], limit=50)
            else:
                rec.product_ids = rec.env['product.template'].search([0, '=', 1])

    def create_product(self):
        product_list = self.env['product.template'].search(['shop_id', '=', self.shop_id], limit=3)
        pro_list = self.env['s.discount.program.product'].search([])
        product_id_list = []
        for product in pro_list:
            if product.discount_id.id == self.id:
                product_id_list.append(product.discount_id.id)
        for product in product_list:
            if product.id not in product_id_list:
                self.env['s.discount.program.product'].create({
                    'discount_id': self.id,
                    'product_id': product.id
                })

    def creat_customer(self):
        # customer_list = self.env['res.partner'].search([('shop_id', '=', self.shop_id.id),
        #                                                 ('company_type', '=', 'person')], limit=3)
        customer_list = self.env['res.partner'].search([('shop_id', '=', self.shop_id.id)], limit=3)
        cus_list = self.env['s.discount.program.customer'].search([])
        customer_id_list = []
        for customer in cus_list:
            if customer.discount_id.id == self.id:
                customer_id_list.append(customer.customer_id.id)
        for customer in customer_list:
            if customer.id not in customer_id_list:
                self.env['s.discount.program.customer'].create({
                    'discount_id': self.id,
                    'customer_id': customer.id
                })

class ShopifyDiscountProgramProduct(models.Model):
    _name = "s.discount.program.product"

    discount_id = fields.Many2one('s.discount.program', string='Discount ID')
    product_id = fields.Many2one('product.template', string='Product ID')
    name = fields.Char(related='product_id.name')
    price = fields.Float(related='product_id.lst_price')
    discount_amount = fields.Float(string='Discount Amount')

class ShopifyDiscountProgramCustomer(models.Model):
    _name = "s.discount.program.customer"

    discount_id = fields.Many2one('s.discount.program', string='Discount ID')
    customer_id = fields.Many2one('res.partner', string='Customer ID')
    email = fields.Char(related='customer_id.email')
    check_person = fields.Boolean(string='Choose Person')