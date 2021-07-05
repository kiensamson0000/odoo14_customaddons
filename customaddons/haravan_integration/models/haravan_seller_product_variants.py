import requests
import json

from odoo import models, fields, api, tools, _


class HaravanSellerProductVariants(models.Model):
    _name = 'haravan.seller.product.variants'
    _description = 'API Products Varians Haravan'

    # /home/kienkhuat/Documents/odoo/addons/product/models/product_template.py    product
    # /home/kienkhuat/Documents/odoo/addons/product/views/product_views.xml
    # /home/kienkhuat/Documents/odoo/addons/product/models/product.py             product_variants

    name = fields.Char(string='Product Name', store=True)
    # seller_product_id = fields.Char(string='Product ID', store=True)
    # image = fields.Binary(store=True)
    # product_type = fields.Char("Product Type")
    # vendor = fields.Char('Company')
    # description = fields.Char()
    # price = fields.Float('Cost')  # null
    # barcode = fields.Char(
    #     'Barcode')  # null     #compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode')

    # def get_products_haravan(self):
    #     try:
    #         # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
    #         token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
    #         url = "https://apis.haravan.com/com/products.json"
    #
    #         payload = ''
    #
    #         headers = {
    #             # 'Authorization': 'Bearer ' + current_seller.token_connect
    #             'Authorization': 'Bearer ' + token_connect
    #         }
    #
    #         response = requests.request("GET", url, headers=headers, data=payload)
    #
    #         result_products = response.json()
    #         list_product = result_products['products']
    #         val = {}
    #         for product in list_product:
    #             if 'id' in product:
    #                 val["seller_product_id"] = product['id']
    #                 val["name"] = product['title']
    #                 val['product_type'] = product['product_type']
    #                 val['vendor'] = product['vendor']
    #                 # list_image = product['images']
    #                 # for image in list_image:
    #                 #     if 'id' in image:
    #                 #         val['image'] = base64.b64encode(urlopen(image["src"]).read())
    #                 existed_product = self.env["haravan.seller.product"].search(
    #                     [('seller_product_id', '=', product['id'])], limit=1)
    #                 if len(existed_product) < 1:
    #                     self.env["haravan.seller.product"].create(val)
    #                 else:
    #                     existed_product.write(val)
    #     except Exception as e:
    #         print(e)
    #
