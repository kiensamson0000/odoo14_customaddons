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
    woo_height = fields.Float(string='Height', default=5)
    woo_length = fields.Float(string='Length', default=20)
    woo_width = fields.Float(string='Width', default=10)
    woo_manage_stock = fields.Boolean(string='Manage Stock', default=True, store=True)
    woo_stock_quantity = fields.Integer(string='Stock Quantity', required=True, default=50)
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
                    vals['woo_product_id'] = data['id']
                    vals['default_code'] = data['sku']
                    vals['name'] = data['name']
                    vals['sale_ok'] = data['on_sale']
                    vals['purchase_ok'] = data['purchasable']
                    vals['type'] = 'product'
                    vals['taxes_id'] = None
                    vals['is_published'] = True
                    vals['woo_date_created'] = data['date_created']
                    vals['woo_date_modified'] = data['date_modified']
                    vals['list_price'] = data['price']
                    vals['check_product_woo'] = True
                    vals['description'] = re.sub(r'<.*?>', '', data['description'])
                    vals['image_1920'] = base64.b64encode(urlopen(data["images"][0]["src"]).read())
                    # 'manage_stock': data['manage_stock']
                    # 'woo_stock_quantity': data['stock_quantity']
                    # 'stock_status': data['stock_status']
                    vals['weight'] = float(data['weight'])
                    vals['woo_height'] = float(data['dimensions']['height'])
                    vals['woo_length'] = float(data['dimensions']['length'])
                    vals['woo_width'] = float(data['dimensions']['width'])
                    # 'parent_id': data['parent_id'],
                    # tag, attributes

                    attrib_line_vals = []
                    if data['attributes']:
                        attrib_line_vals = self.prepare_attribute_vals(data)
                    if len(attrib_line_vals) > 0:
                        vals['attribute_line_ids'] = attrib_line_vals

                    existed_product = self.env['product.template'].search(
                    [('woo_product_id', '=', data['id'])], limit = 1)
                    if len(existed_product) < 1:
                        self.env['product.template'].create(vals)
                    else:
                        existed_product.write(vals)
        except Exception as e:
            raise ValidationError(str(e))

    ### VARIENTS_PRODUCT
    def prepare_attribute_vals(self, result):
        product_attribute_obj = self.env['product.attribute']
        product_attribute_value_obj = self.env['product.attribute.value']
        attrib_line_vals = []
        if 'attributes' in result:
            for attrib in result.get('attributes'):
                attrib_name = attrib.get('name')
                attrib_values = attrib.get('options')
                attr_val_ids = []
                attribute = product_attribute_obj.search([('name', '=ilike', attrib_name)], limit=1)
                if not attribute:
                    attribute = product_attribute_obj.create({'name': attrib_name})
                for attrib_vals in attrib_values:
                    attrib_value = attribute.value_ids.filtered(lambda x: x.name == attrib_vals)
                    if attrib_value:
                        attr_val_ids.append(attrib_value[0].id)
                    else:
                        attrib_value = product_attribute_value_obj.with_context(active_id=False).create(
                            {'attribute_id': attribute.id, 'name': attrib_vals})
                        attr_val_ids.append(attrib_value.id)
            if attr_val_ids:
                attribute_line_ids_data = [0, 0,
                                           {'attribute_id': attribute.id, 'value_ids': [[6, 0, attr_val_ids]]}]
                attrib_line_vals.append(attribute_line_ids_data)
        return attrib_line_vals

