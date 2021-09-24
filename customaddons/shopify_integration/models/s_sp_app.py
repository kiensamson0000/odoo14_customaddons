# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SSpApp(models.Model):
    _name = 's.sp.app'
    _description = 'save shop that have installed the app'

    sp_api_key = fields.Char('API Key')
    sp_secret_key = fields.Char('Secret Key')
    sp_api_version = fields.Char('API Version')
    sp_app_name = fields.Char('App name')