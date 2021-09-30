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
from urllib.request import urlopen
import base64

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
            # todo: create s_shop
            shops_list = request.env['s.shop'].search([])
            new_shop = True
            password = random.randint(1000000000, 9999999999)
            print(password)
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

                # todo: create s_sp_app
                request.env['s.sp.app'].sudo().create({
                    'sp_app': request.env['s.app'].search([('s_api_key', '=', exiting_app.s_api_key)]).id,
                    'sp_shop': request.env['s.shop'].search([('shop_base_url', '=', shop_current.domain)]).id,
                    'token_shop_app': access_token,
                    'web_user': shop_current.domain,
                })

                # todo: create shop in 'res.partner'
                existed_res_partner = request.env['res.partner'].search([('email', '=', shop_current.customer_email)])
                partner_vals = {
                    'company_type': 'company',
                    'name': shop_current.name,
                    'street': shop_current.address1,
                    'street2': shop_current.address2,
                    'city': shop_current.city,
                    'zip': shop_current.zip,
                    'email': shop_current.customer_email,
                    'website': shop_current.domain,
                    'shop_id': request.env['s.shop'].search([("shop_base_url", "=", shop_current.domain)]).id,
                }
                if not existed_res_partner:
                    request.env['res.partner'].sudo().create(partner_vals)
                else:
                    request.env['res.partner'].sudo().write(partner_vals)

                # todo: create user in 'res.partner'
                existed_user = request.env['res.users'].search([('login', '=', shop_current.domain)])
                user_vals = {
                    'login': shop_current.domain,
                    'password': password,
                    'active': 'true',
                    'partner_id': request.env['res.partner'].sudo().search([('email', '=', shop_current.customer_email)]).id
                }
                print('shdsadgjsd')
                print(user_vals)
                if not existed_user:
                    request.env['res.users'].sudo().create(user_vals)
                else:
                    request.env['res.users'].sudo().write(user_vals)

            # todo: create customer in 'res.partner'
            website = 'https://' + shop_current.domain
            customer_current = shopify.Customer.search()
            customer_list = request.env['res.partner'].search([])
            customer_id_list = []
            for customer in customer_list:
                customer_id_list.append(customer.customer_id)
            for customer in customer_current:
                if customer.id.__str__() not in customer_id_list:
                    customer_name = customer.first_name + '' + customer.last_name
                    cus_vals = {
                        'customer_id': customer.id,
                        'company_type': 'person',
                        'name': customer_name,
                        'parent_id': request.env['res.partner'].search([("website", "=", website)]).id,
                        'phone': customer.phone,
                        'email': customer.email,
                        'shop_id': request.env['s.shop'].search([("shop_base_url", "=", shop_current.domain)]).id
                    }
                    request.env['res.partner'].create(cus_vals)

            # todo: create product in 'product.template'
            # product_current = shopify.Product.find()
            # for product in product_current:
            #     product_vals = {
            #         'pro_id': product.id,
            #         'name': product.title,
            #         'lst_price': product.variants[0].price,
            #         'variant_id': product.variants[0].id,
            #         'image_1920': base64.b64encode(urlopen(product.images[0].src).read()),
            #         'shop_id': request.env['s.shop'].search([("shop_base_url", "=", shop_current.domain)]).id
            #     }
            #     existed_product = request.env["product.template"].sudo().search([('pro_id', '=', product.id)],
            #                                                           limit=1)
            #     if not existed_product:
            #         request.env['product.template'].sudo().create(product_vals)
            #     else:
            #         existed_product.write(product_vals)
            password_login = request.env['s.shop'].search([('shop_base_url', '=', shop_current.domain)])
            print(password_login.shop_password)
            #
            # todo: insert script theme
            script_src = "https://odoo.website/shopify_integration/static/src/js/shop_script.js"
            existedScriptTags = shopify.ScriptTag.find(src=script_src)
            if not existedScriptTags:
                shopify.ScriptTag.create({
                    "event": "onload",
                    "src": script_src
                })
            ####
            curent_user = request.env['s.shop'].search([('shop_base_url', '=', shop_current.domain)])
            db = http.request.env.cr.dbname
            request.env.cr.commit()
            request.session.authenticate(db, curent_user.shop_base_url, curent_user.shop_currency)
            redirect_link = 'https://odoo.website/web#cids=1&home='
            # redirect_link = 'https://odoo.website/web#id=' + password_login.id.__str__() + '&action=301&model=shopify.shop&view_type=form&cids=1&menu_id=213'
            return werkzeug.utils.redirect(redirect_link)

    @http.route('/shopify_data/fetch_product/<string:product_id>/<string:vendor>/<string:shop>', auth='public',
                type='json', cors='*', csrf=False)
    def odoo_fetch_product(self, product_id, vendor, shop, **kw):
        shopify_product = request.env['product.template'].search([('pro_id', '=', product_id)])
        shop_id = request.env['s.shop'].search([('shop_base_url', '=', shop)])
        discount_product = request.env['s.discount.program'].search([('shop_id', '=', shop_id.id)])
        discount_pro = 0
        for discount in discount_product.product_ids:
            if discount.product_id.id == shopify_product.id:
                discount_pro = discount.discount_amount
                break
        return {
            'product_info': shopify_product,
            'product_name': shopify_product.name,
            'product_price': shopify_product.lst_price,
            'product_variant': shopify_product.variant_id,
            'discount': discount_pro,
            'shop': shop,
        }

    @http.route('/shopify_data/fetch_variant/<string:variant_id>/<string:shop>', auth='public',
                type='json', cors='*', csrf=False)
    def odoo_fetch_variant(self, variant_id, shop, *kwargs):
        variant = variant_id.split(',')
        pro_list = []
        pro_list_name = []
        for var in variant[:-1]:
            sp_product = request.env['product.template'].sudo().search([('variant_id', '=', var)])
            pro_list.append(sp_product.id)
            pro_list_name.append(sp_product.name)

        shop_id = request.env['s.shop'].sudo().search([('shop_base_url', '=', shop)])
        discount_product = request.env['s.discount.program'].sudo().search([('shop_id', '=', shop_id.id)])
        discount = 0

        dict_discount_product = {}
        discount_product_list = []
        for discount_pro in discount_product:
            discount_name = discount_pro.name
            discount_product_list.append(discount_pro.name)
            dict_discount_product[discount_name] = {}
            for pro in discount_pro.product_ids:
                if pro.product_id.id in pro_list:
                    dict_discount_product[discount_name][pro.name] = pro.discount_amount

        dict_discount = {}
        for pro in pro_list_name:
            price_list = []
            for dis in discount_product_list:
                price_list.append(dict_discount_product[dis][pro])
            price_max = max(price_list)
            for dis in discount_product_list:
                if (price_max > 0) & (dict_discount_product[dis][pro] == price_max):
                    dict_discount[pro] = {'Discount Name': dis, 'Discount Amount': price_max}
                    discount += price_max
                    break
        return {
            'discount': dict_discount,
            'total': discount
        }
