# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SShop(models.Model):
    _name = 's.shop'
    _description = 'save list shops'

    shop_base_url = fields.Char('Base Url')
    shop_owner = fields.Char('Shop owner')
    shop_currency = fields.Char('Currency')
    shop_password = fields.Char('Password')