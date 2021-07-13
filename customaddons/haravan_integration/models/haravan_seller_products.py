import requests
import json
from urllib.request import urlopen
import base64

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError


class HaravanSellerProduct(models.Model):
    _name = 'haravan.seller.product'
    _description = 'API Products Haravan'

    seller_product_id = fields.Char(string='Product ID', store=True)
    name = fields.Char(string='Product Name', store=True)
    image_url = fields.Char(store=True)  # save url image --> (widget="image" view)
    product_type = fields.Char("Product Type")
    tags = fields.Char("Tag")
    vendor = fields.Char('Company')
    description = fields.Char()
    price = fields.Float('Cost')
    barcode = fields.Char('Barcode')
    created_at = fields.Char('Created at')
    updated_at = fields.Char('Updated at')
    check_product = fields.Boolean(compute='_compute_check_product_haravan')
    list_product = fields.Text()  # add 1 field save get_data_product of file json

    # create add fields to create/update product
    tags = fields.Char("Tag")
    image = fields.Char("Image")

    def _compute_check_product_haravan(self):
        for rec in self:
            if rec.seller_product_id:
                rec.check_product = True
            else:
                rec.check_product = False

    #############################
    ## USE API PRODUCT ON Module "Haravan Integration"
    def get_products_haravan(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products.json"
            payload = {}
            headers = {
                #'Authorization': 'Bearer ' + current_seller.token_connect
                'Authorization': 'Bearer ' + token_connect
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            result_products = response.json()
            list_product = result_products['products']
            val = {}
            if list_product:
                for product in list_product:
                    if 'id' in product:
                        val['seller_product_id'] = product['id']
                        val['name'] = product['title']
                        val['product_type'] = product['product_type']
                        val['vendor'] = product['vendor']
                        val['tags'] = product['tags']
                        val['created_at'] = product['created_at']
                        val['updated_at'] = product['updated_at']
                        # val['image'] = base64.b64encode(urlopen(product["images"][1]["src"]).read())
                        if product['images']:  # xu ly de check values = null
                            for image in product['images']:
                                if 'id' in image:
                                    val['image_url'] = product["images"][0]["src"]
                        existed_product = self.env["haravan.seller.product"].search(
                            [('seller_product_id', '=', product['id'])], limit=1)
                        if not existed_product:
                            self.env["haravan.seller.product"].create(val)
                        else:
                            existed_product.write(val)
        except Exception as e:
            print(e)

    ####### chua xu ly variant cua product
    def create_products_haravan(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products.json"
            payload = json.dumps({
                "product": {
                    "title": self.name,
                    "body_html": self.description,
                    "vendor": self.vendor,
                    "product_type": self.product_type,
                    "tags": self.tags,
                    "images": [
                        {
                            "src": self.image
                        }
                    ],
                    "variants": [
                        # {
                        #     "option1": "Blue",
                        #     "option2": "155",
                        #     "price": "100",
                        #     "sku": 123,
                        #     "inventory_policy": "deny",
                        #     "inventory_management": null,
                        #     "requires_shipping": false, "barcode": "ss",
                        #     "compare_at_price": 1500,
                        #     "grams": 550
                        # },
                        # {
                        #     "option1": "Black",
                        #     "option2": "159",
                        #     "price": "200",
                        #     "sku": "123",
                        #     "inventory_policy": "continue",
                        #     "inventory_management": "haravan",
                        #     "requires_shipping": true,
                        #     "barcode": "qqq",
                        #     "compare_at_price": 1500,
                        #     "grams": 200
                        # }
                    ],
                    "options": [
                        # {
                        #     "name": "Color"
                        # },
                        # {
                        #     "name": "Size"
                        # }
                    ]
                }
            })
            headers = {
                # 'Authorization': 'Bearer ' + current_seller.token_connect
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token_connect
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)  # check
            if response.json()['product']:
                print(response.json()['product'])
                self.seller_product_id = response.json()['product']['id']  # save seller_product_id on database
            else:
                raise ValidationError(_('Create Product Fail in Sync with API Haravan'))
        except Exception as e:
            print(e)

    ####UPDATE
    ####
    ######################
    def update_products_haravan(self):
        pass

    #### button "save": 2 action(create and cearte api)
    # @api.model
    # def create(self, vals):
    #     res = super(HaravanSellerProduct, self).create(vals)
    #     #call API creat product vao button save(create)
    #     self.create_products_haravan()
    #     return res

    ###### API DELETE 1 PRODUCT FOLLOW ID
    def delete_products_haravan(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products/" + self.seller_product_id + ".json"
            payload = json.dumps({
                "product": {
                    "id": self.seller_product_id
                }
            })
            headers = {
                # 'Authorization': 'Bearer ' + current_seller.token_connect
                'Authorization': 'Bearer ' + token_connect
            }
            response = requests.request("DELETE", url, headers=headers, data=payload)
            print(response.text)  # CHECK
            if response.json()['error']:
                raise ValidationError(_('Sản phẩm không tồn tại'))
        except Exception as e:
            print(e)


    #############################
    ## USE API PRODUCT "HARAVAN" ON APP "SALES"
    def get_product_haravan_sale(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products.json"
            payload = {}
            headers = {
                #'Authorization': 'Bearer ' + current_seller.token_connect
                'Authorization': 'Bearer ' + token_connect
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            result_products = response.json()
            list_product = result_products['products']
            val = {}
            for product in list_product:
                if 'id' in product:
                    ### link ref to categories, company
                    ### Note: get "category,company" trước nếu không bị error
                    existed_cate_product = self.env['product.category'].search(
                        [('name', '=', product['product_type'])], limit=1)
                    if existed_cate_product:
                        val['categ_id'] = existed_cate_product.id

                    ### API get product ko tra ve ten company nen ko the search lay ten company de hien thi nhu categories
                    # existed_company = self.env['res.company'].search([('name', '=', companies['name'])], limit=1)
                    # val['company_id'] = existed_company_product.id

                    # field of 'product.template'
                    val['name'] = product['title']
                    # val['type'] = 'product'
                    val['sale_ok'] = True
                    val['purchase_ok'] = False
                    val['description'] = product['body_html']
                    val['default_code'] = product['id']
                    val['taxes_id'] = None
                    val['is_published'] = True  # field in model Webiste(Shop) pulish product
                    # standard_price
                    # list_price
                    # barcode

                    # field new add (product.template)
                    val['haravan_product_id'] = product['id']
                    val['haravan_product_type'] = product['product_type']
                    val['haravan_tags'] = product['tags']
                    val['haravan_created_at'] = product['created_at']
                    val['haravan_updated_at'] = product['updated_at']
                    if product['images']:  # xu ly de check values = null
                        for image in product['images']:
                            if 'id' in image:
                                val['haravan_image_url'] = product["images"][0]["src"]
                                # error don't read url image
                                # reason: url private
                                # val['image_1920'] = base64.b64encode(urlopen(product["images"][0]["src"]).read())
                    existed_product = self.env["product.template"].search([('haravan_product_id', '=', product['id'])],
                                                                          limit=1)
                    if not existed_product:
                        self.env["product.template"].sudo().create(val)
                    else:
                        existed_product.write(val)
        except Exception as e:
            print(e)

    ##### XU LY VARIENT CUA PRODUCT
    ################
    # def prepare_attribute_vals(self, result):
    #     product_attribute_obj = self.env['product.attribute']
    #     product_attribute_value_obj = self.env['product.attribute.value']
    #     attrib_line_vals = []
    #     if 'options' in result:
    #         for attrib in result.get('options'):
    #             attrib_name = attrib.get('name')
    #             attrib_values = attrib.get('values')
    #             attr_val_ids = []
    #             attribute = product_attribute_obj.search([('name', '=ilike', attrib_name)], limit=1)
    #             if not attribute:
    #                 attribute = product_attribute_obj.create({'name': attrib_name})
    #             for attrib_vals in attrib_values:
    #                 attrib_value = attribute.value_ids.filtered(lambda x: x.name == attrib_vals)
    #                 if attrib_value:
    #                     attr_val_ids.append(attrib_value[0].id)
    #                 else:
    #                     attrib_value = product_attribute_value_obj.with_context(active_id=False).create(
    #                         {'attribute_id': attribute.id, 'name': attrib_vals})
    #                     attr_val_ids.append(attrib_value.id)
    #             if attr_val_ids:
    #                 attribute_line_ids_data = [0, 0,
    #                                            {'attribute_id': attribute.id, 'value_ids': [[6, 0, attr_val_ids]]}]
    #                 attrib_line_vals.append(attribute_line_ids_data)
    #     return attrib_line_vals