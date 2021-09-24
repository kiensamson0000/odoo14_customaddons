# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import shopify
import binascii
import os
import werkzeug
from werkzeug.utils import redirect
from werkzeug.http import dump_cookie
import random
import string

class ShopifyApp(http.Controller):
    @http.route('/shopify/auth/<string:name>', auth='public', website=False)
    def shopify_auth(self, name=None, **kw):
        exiting_app = http.request.env['s.app'].sudo().search([('s_app_name', '=', name)])
        if 'shop' in kw:
            shop_url = kw['shop']
            print(kw)
            shopify.Session.setup(api_key=exiting_app.s_api_key, secret=exiting_app.s_secret_key)
            base_url = "https://odoo.website"
            session = shopify.Session(shop_url, exiting_app.s_api_version, kw)
            scope = ['read_orders', 'write_products', 'read_customers', 'write_script_tags', 'read_script_tags']
            redirect_uri = base_url + "/shopify/finalize/" + name
            permission_url = session.create_permission_url(scope, redirect_uri)
            print(permission_url)
        return werkzeug.utils.redirect(permission_url)

    @http.route('/shopify/finalize/<string:name>', auth='public', website=True)
    def shopify_finalize(self, name=None, **kw):
        exiting_app = http.request.env['s.app'].sudo().search([('s_app_name', '=', name)])
        if 'shop' in kw:
            shop_url = kw['shop']
            shopify.Session.setup(
                api_key=exiting_app.s_api_key,
                secret=exiting_app.s_secret_key)
            session = shopify.Session(shop_url, exiting_app.s_api_version)
            access_token = session.request_token(kw)
            #
            session = shopify.Session(shop_url, exiting_app.s_api_version, access_token)
            shopify.ShopifyResource.activate_session(session)
            #
            #create s_shop
            shops_list = request.env['s.shop'].search([])
            new_shop = True
            password = random.randint(1000000000, 9999999999)
            shop_current = shopify.Shop.current()
            for shop in shops_list:
                if shop_current.myshopify_domain == shop.shop_base_url:
                    new_shop = False
                    break
            if new_shop:
                request.env['s.shop'].sudo().create({
                    'shop_base_url': shop_current.domain,
                    'shop_owner': shop_current.shop_owner,
                    'shop_currency': password,
                })
            #
            #create s_sp_app
            request.env['s.sp.app'].sudo().create({
                'sp_app': request.env['s.app'].search([('s_api_key', '=', exiting_app.s_api_key)]).id,
                'sp_shop': request.env['s.shop'].search([('shop_base_url', '=', shop_current.domain)]).id,
            })
            #
            #create infor users
            partner_id = request.env['res.partner'].sudo().create({
                'company_type': 'company',
                'name': shop_current.name,
                'street': shop_current.address1,
                'street2': shop_current.address2,
                'city': shop_current.city,
                'zip': shop_current.zip,
                'email': shop_current.customer_email,
                'website': shop_current.domain,
                'shop_id': request.env['s.shop'].search([("shop_base_url", "=", shop_current.domain)]).id
            })
            request.env['res.users'].sudo().create({
                'login': shop_current.domain,
                'password': password,
                'active': 'true',
                'partner_id': partner_id.id,
            })
            #
            #create customer
            customer = shopify.Customer.search()
            # customer_list = request.


