# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Sale(models.Model):
    _inherit = "sale.order"
    _description = "Sale Inherit"

    sale_description = fields.Char(string="Sale Description")



