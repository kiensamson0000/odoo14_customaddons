import requests
import json
from odoo import fields, models, api


class HaravanSeller(models.Model):
    _name = "haravan.seller"
    _description = "Information Seller Haravan"

    code = fields.Char('Code')

    client_id = fields.Char('Client ID')

    client_secret = fields.Char('Client Secret')

    grant_type = fields.Char('Grant type')

    redirect_uri = fields.Char('Redirect uri')

    token_connect = fields.Char('Token Seller')