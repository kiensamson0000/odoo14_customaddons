import requests
import json
from datetime import *
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from urllib.request import urlopen
import base64
import re


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"
    _description = "Inherit product template"

    woo_product_id = fields.Char(string='Product ID', store=True)
    haravan_product_type = fields.Char("Product Type")
    # haravan_tags = fields.Char("Tag")
    # haravan_image_url = fields.Char(store=True)  # save url image --> hien thi trong view = (widget="image") #1
    woo_date_created = fields.Char('Created at')
    woo_date_modified = fields.Char('Updated at')
    check_product_woo = fields.Boolean()

    def get_product_woocommerce(self):
        try:
            current_seller = self.env['woocommerce.seller'].sudo().search([])[0]
            url = str(current_seller.link_website) + "wp-json/wc/v3/products?consumer_key=" + str(
                current_seller.consumer_key) + "&consumer_secret=" + str(current_seller.consumer_secret)
            payload = {}
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            list_products = response.json()
            vals = {}
            for data in list_products:
                if 'id' in data:
                    vals = {
                        'woo_product_id': data['id'],
                        'default_code': data['sku'],
                        'name': data['name'],
                        'sale_ok': data['on_sale'],
                        'purchase_ok': data['purchasable'],
                        'type': 'product',
                        'taxes_id': None,
                        'is_published': True,
                        'woo_date_created': data['date_created'],
                        'woo_date_modified': data['date_modified'],
                        'list_price': data['price'],
                        'check_product_woo': True,
                        # 'status': data['status'],
                        'description': re.sub(r'<.*?>', '', data['description']),
                        'image_1920': base64.b64encode(urlopen(data["images"][0]["src"]).read()),
                        # 'manage_stock': data['manage_stock'],
                        # 'stock_quantity': data['stock_quantity'],
                        # 'stock_status': data['stock_status'],
                        # 'backorders': data['backorders'],
                        # 'backorders_allowed': data['backorders_allowed'],
                        # 'backordered': data['backordered'],
                        # 'sold_individually': data['sold_individually'],
                        # 'weight': data['weight'],
                        # 'shipping_required': data['shipping_required'],
                        # 'shipping_taxable': data['shipping_taxable'],
                        # 'shipping_class': data['shipping_class'],
                        # 'shipping_class_id': data['shipping_class_id'],
                        # 'reviews_allowed': data['reviews_allowed'],
                        # 'average_rating': data['average_rating'],
                        # 'rating_count': data['rating_count'],
                        # 'parent_id': data['parent_id'],
                        # 'purchase_note': data['purchase_note'],
                    }
                    existed_product = self.env['product.template'].search(
                        [('woo_product_id', '=', data['id'])], limit=1)
                    if len(existed_product) < 1:
                        self.env['product.template'].create(vals)
                    else:
                        existed_product.write(vals)
        except Exception as e:
            raise ValidationError(str(e))


# #   Link To Sendo Categories
#                     for cate in product['categories']:
#                         if cate['is_primary'] == 1:
#                             category_tiki = cate['id']
#                             existed_categories_product = self.env['product.category'].search(
#                                 [('tiki_cate_id', '=', int(category_tiki))], limit=1)
#                             val['categ_id'] = int(existed_categories_product.id)
#                             val['tiki_product_id'] = product['id']
#                             val['name'] = product['name']
#                             val['tiki_category_id'] = int(category_tiki)
#                             val['tiki_status'] = str(product['status'])

#                             val['tiki_type'] = product['type']

#                             val['standard_price'] = product['price']
#                             val['tiki_iventory_type'] = str(product['inventory']['type'])
#                             val['tiki_inventory_quantity'] = product['inventory']['quantity']
#                             val['tiki_inventory_qty'] = product['inventory']['qty']
#                             val['tiki_inventory_qty_available'] = product['inventory']['qty_available'] or 0
#                             val['tiki_fulfillment_type'] = product['inventory']['fulfillment_type']
