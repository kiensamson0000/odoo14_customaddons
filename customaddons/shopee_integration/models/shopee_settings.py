# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ShopeeSettings(models.Model):
    _name = 'shopee.settings'
    _description = 'Shopee Setting'

    setting = fields.Char(string="Setting", required=True)



