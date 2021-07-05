import requests
import json
from urllib.request import urlopen
import base64

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError


class HaravanSellerProduct(models.Model):
    _name = 'haravan.seller.product'
    _description = 'API Products Haravan'

    # /home/kienkhuat/Documents/odoo/addons/product/models/product_template.py    product
    # /home/kienkhuat/Documents/odoo/addons/product/views/product_views.xml
    # /home/kienkhuat/Documents/odoo/addons/product/models/product.py             product_variants

    seller_product_id = fields.Char(string='Product ID', store=True)
    name = fields.Char(string='Product Name', store=True)
    image_url = fields.Char(store=True)  # save url image --> hien thi trong view = (widget="image")
    backup_get_product_data = fields.Text()  # add 1 field to  save get_data of file json
    product_type = fields.Char("Product Type")
    vendor = fields.Char('Company')
    description = fields.Char()
    price = fields.Float('Cost')  # null
    barcode = fields.Char(
        'Barcode')  # null     #compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode')
    created_at = fields.Char('Created at')
    updated_at = fields.Char('Updated at')
    list_product = fields.Text()  # add 1 field save get_data_product of file json

    # create fields to create/update product
    tags = fields.Char("Tag")
    image = fields.Char("Image")

    #####
    ##
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
            for product in list_product:
                if 'id' in product:
                    val['seller_product_id'] = product['id']
                    val['name'] = product['title']
                    val['product_type'] = product['product_type']
                    val['vendor'] = product['vendor']
                    val['created_at'] = product['created_at']
                    val['updated_at'] = product['updated_at']
                    # val['image'] = base64.b64encode(urlopen(product["images"][1]["src"]).read())

                    if 'images' is None:  # xu ly de check values = null
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

    ####### tao wizard trong action
    ####### giong nhu cac nut trong action(khi chon create/update trong action --> auto run)
    def create_products_haravan(self):  # create/update
        # try:
        # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
        token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'

        ####### xu ky truong hop ID khi create/update bi trung => can't create/update

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
                "variants": [],
                "options": []
            }
        })
        headers = {
            # 'Authorization': 'Bearer ' + current_seller.token_connect
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token_connect
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)

        # for list_product in response.json()["products"]:
        #     if 'id' in list_product:
        #         pass
        #     else:
        #         raise ValidationError(_('Error create/update product!'))

    # except Exception as e:
    #     print(e)

    ####### tao wizard trong action
    ###
    def update_products_haravan(self):  # update
        # try:
        # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
        token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'

        ####### xu ky truong hop ID khi create/update bi trung => can't create/update

        url = "https://apis.haravan.com/com/products/" + self.seller_product_id + ".json"
        payload = json.dumps({
            "product": {
                "body_html": self.description,
                "id": 1020104002,
                "images": [],
                "product_type": self.product_type,
                "tags": self.tags,
                "title": self.name,
                "variants": [
                    {
                        "barcode": self.barcode,
                        "compare_at_price": 1500,
                        "fulfillment_service": null,
                        "grams": 550,
                        "id": 1040046883,
                        "inventory_management": null,
                        "inventory_policy": "deny",
                        "inventory_quantity": 0, "old_inventory_quantity": 0,
                        "inventory_quantity_adjustment": null,
                        "position": 1,
                        "price": 100,
                        "product_id": 1020104002,
                        "requires_shipping": false,
                        "sku": "123",
                        "title": "Blue / 155",
                        "image_id": null,
                        "option1": "Blue",
                        "option2": "155",
                        "option3": null,
                        "inventory_advance": null
                    },
                    {
                        "barcode": self.barcode,
                        "compare_at_price": 1500,
                        "fulfillment_service": null,
                        "grams": 200,
                        "id": 1040046884,
                        "inventory_management": "haravan",
                        "inventory_policy": "continue",
                        "inventory_quantity": 0,
                        "old_inventory_quantity": 0,
                        "inventory_quantity_adjustment": null,
                        "position": 2,
                        "price": 200,
                        "product_id": 1020104002,
                        "requires_shipping": true,
                        "sku": "123",
                        "taxable": false,
                        "title": "Black / 159",
                        "updated_at": "2019-05-31T09:12:00.55Z",
                        "image_id": null,
                        "option1": "Black",
                        "option2": "159",
                        "option3": null,
                        "inventory_advance": null
                    }
                ],
                "vendor": self.vendor,
                "options": [
                    {"name": "Color",
                     "id": 2051366797,
                     "position": 1,
                     "product_id": 1020104002
                     },
                    {
                        "name": "Size",
                        "id": 2051366798,
                        "position": 2,
                        "product_id": 1020104002
                    }
                ],
            }
        })
        headers = {
            # 'Authorization': 'Bearer ' + current_seller.token_connect
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token_connect
        }
        response = requests.request("POST", url, headers=headers, data=payload)
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

    ####### tao wizard trong action
    ###### API dùng để xóa 1 sản phẩn theo id
    ###### Tao 2 field, 1 filed many2one id, 1 filed ten san pham ==> chon(search) 1 id => ten san pham (muc dich: check lai ten san pham dung chua moi xoa)
    def delete_products_haravan(self):
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
