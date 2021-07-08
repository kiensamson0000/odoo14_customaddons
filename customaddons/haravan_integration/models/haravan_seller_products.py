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
    image_url = fields.Char(store=True)  # save url image --> hien thi trong view = (widget="image")
    backup_get_product_data = fields.Text()  # add 1 field to  save get_data of file json
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
    ## USE API PRODUCT ON Module Haravan Integration
    #############################
    def get_products_haravan(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products.json"
            payload = {}
            headers = {
                # 'Authorization': 'Bearer ' + current_seller.token_connect
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

    ####### chua xu ly variant cuar product
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
                self.seller_product_id = int(response.json()['product']['id'])  # save seller_product_id on database
            else:
                raise ValidationError(_('Create Product Fail in Sync with API Haravan'))
        except Exception as e:
            print(e)





    ####UPDATE
    ############################################3
    # def update_products_haravan(self):
    #     # try:
    #     # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
    #     token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
    #
    #     ####### xu ky truong hop ID khi create/update bi trung => can't create/update
    #
    #     url = "https://apis.haravan.com/com/products/" + self.seller_product_id + ".json"
    #     payload = json.dumps({
    #         "product": {
    #             "body_html": self.description,
    #             "id": 1020104002,
    #             "images": [],
    #             "product_type": self.product_type,
    #             "tags": self.tags,
    #             "title": self.name,
    #             "variants": [
    #                 {
    #                     "barcode": self.barcode,
    #                     "compare_at_price": 1500,
    #                     "fulfillment_service": null,
    #                     "grams": 550,
    #                     "id": 1040046883,
    #                     "inventory_management": null,
    #                     "inventory_policy": "deny",
    #                     "inventory_quantity": 0, "old_inventory_quantity": 0,
    #                     "inventory_quantity_adjustment": null,
    #                     "position": 1,
    #                     "price": 100,
    #                     "product_id": 1020104002,
    #                     "requires_shipping": false,
    #                     "sku": "123",
    #                     "title": "Blue / 155",
    #                     "image_id": null,
    #                     "option1": "Blue",
    #                     "option2": "155",
    #                     "option3": null,
    #                     "inventory_advance": null
    #                 },
    #                 {
    #                     "barcode": self.barcode,
    #                     "compare_at_price": 1500,
    #                     "fulfillment_service": null,
    #                     "grams": 200,
    #                     "id": 1040046884,
    #                     "inventory_management": "haravan",
    #                     "inventory_policy": "continue",
    #                     "inventory_quantity": 0,
    #                     "old_inventory_quantity": 0,
    #                     "inventory_quantity_adjustment": null,
    #                     "position": 2,
    #                     "price": 200,
    #                     "product_id": 1020104002,
    #                     "requires_shipping": true,
    #                     "sku": "123",
    #                     "taxable": false,
    #                     "title": "Black / 159",
    #                     "updated_at": "2019-05-31T09:12:00.55Z",
    #                     "image_id": null,
    #                     "option1": "Black",
    #                     "option2": "159",
    #                     "option3": null,
    #                     "inventory_advance": null
    #                 }
    #             ],
    #             "vendor": self.vendor,
    #             "options": [
    #                 {"name": "Color",
    #                  "id": 2051366797,
    #                  "position": 1,
    #                  "product_id": 1020104002
    #                  },
    #                 {
    #                     "name": "Size",
    #                     "id": 2051366798,
    #                     "position": 2,
    #                     "product_id": 1020104002
    #                 }
    #             ],
    #         }
    #     })
    #     headers = {
    #         # 'Authorization': 'Bearer ' + current_seller.token_connect
    #         'Content-Type': 'application/json',
    #         'Authorization': 'Bearer ' + token_connect
    #     }
    #     response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)

    # for list_product in response.json()["products"]:
    #     if 'id' in list_product:
    #         pass
    #     else:
    #         raise ValidationError(_('Error create/update product!'))

    # except Exception as e:
    #     print(e)

    #### button "save": 2 action(create and cearte api)
    # @api.model
    # def create(self, vals):
    #     res = super(HaravanSellerProduct, self).create(vals)
    #
    #     #call API creat product vao button save(create)
    #     self.create_products_haravan()
    #
    #     return res



    ###### API dùng để xóa 1 sản phẩn theo id
    ###DELETE
    ######
    def delete_products_haravan(self):
    # try:
        # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
        token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
        url = "https://apis.haravan.com/com/products/" + self.seller_product_id + ".json"
        payload = {}
        headers = {
            # 'Authorization': 'Bearer ' + current_seller.token_connect
            # 'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token_connect
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        # print(response.text)
        if response.json()['error']:
            raise ValidationError(_('Sản phẩm không tồn tại'))
    # except Exception as e:
    #     print(e)










    #############################
    ## USE API PRODUCT "HARAVAN" ON APP "SALES"
    #############################
    def get_product_haravan_sale(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products.json"
            payload = {}
            headers = {
                # 'Authorization': 'Bearer ' + current_seller.token_connect
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

                    ### categories chưa tự ăn vào
                    existed_cate_product = self.env['product.category'].search(
                        [('name', '=', product['product_type'])], limit=1)
                    # if 'categ_id' in existed_cate_product:
                    val['categ_id'] = existed_cate_product.id

                    ### API get product ko tra ve ten company nen ko the search lay ten company de hien thi nhu categories
                    # existed_company = self.env['res.company'].search([('name', '=', companies['name'])], limit=1)
                    # val['company_id'] = existed_company_product.id

                    # field có sẵn in core
                    val['name'] = product['title']
                    # val['type'] = 'product'
                    val['sale_ok'] = True
                    val['purchase_ok'] = False
                    val['description'] = product['body_html']
                    val['taxes_id'] = None
                    val['is_published'] = True  # field in model Webiste(Shop) pulish product
                    # standard_price
                    # list_price
                    # default_code   tuong duong sku sanpham bien the (chua xu ly duoc)
                    # barcode
                    # company_id "xu ly giong categories"

                    # field add khi core không có sẵn
                    val['haravan_product_id'] = product['id']
                    val['haravan_product_type'] = product['product_type']
                    # val['haravan_tags'] = product['tags']
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
