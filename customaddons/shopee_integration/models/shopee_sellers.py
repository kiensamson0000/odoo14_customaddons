# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ShopeeSellers(models.Model):
    _name = 'shopee.sellers'
    _description = 'Shopee Sellers'

    seller = fields.Char(string="Seller Name")



