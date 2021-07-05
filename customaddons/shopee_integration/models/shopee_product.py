# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ShopeeProduct(models.Model):
    _name = 'shopee.product'
    _description = 'Shopee Product'

    itemid = fields.Char(string="Item ID", required=True)
    shopid = fields.Char(string="Shop ID", required=True)
    shop_name = fields.Text(string="Shop name")
    name = fields.Char(string="Product Name")
    item_status = fields.Text(string="Status")   #values: normal or sold_out
    brand = fields.Char(string="Brand")
    # price = fields.Monetary(string="Price")
    # categories = fields.Many2many()
    description = fields.Char(string="Product Description")
    discount = fields.Float(string="Discount")


