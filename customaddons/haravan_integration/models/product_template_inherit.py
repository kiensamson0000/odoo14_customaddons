import requests
import json

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    _description = 'Inherit product template'

    ##### xoa bo ca field thua da co trong core

    haravan_product_id = fields.Char(string='Product ID', store=True)
    haravan_product_type = fields.Char("Product Type")
    haravan_tags = fields.Char("Tag")
    haravan_image_url = fields.Char(store=True)  # save url image --> hien thi trong view = (widget="image") #1
    haravan_price = fields.Float('Cost')  # null
    haravan_barcode = fields.Char(
        'Barcode')  # null #compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode')
    haravan_created_at = fields.Char('Created at')
    haravan_updated_at = fields.Char('Updated at')
    check_product_haravan = fields.Boolean(compute='_compute_check_product')

    ### add 1 field 'quantity'
    ### add 1 field ma giam gia (khuyen mai)
    ### NOTE XU LY 1 so dieu kien cho field

    def _compute_check_product(self):
        for rec in self:
            if rec.haravan_product_id:
                rec.check_product_haravan = True
            else:
                rec.check_product_haravan = False

    ####### chua xu ly dươc variant chung với product
    def create_products_sales(self):
        # try:
        # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
        token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
        url = "https://apis.haravan.com/com/products.json"

        # chu y phai an vao cac truong field
        payload = json.dumps({
            "product": {
                "title": self.name,
                "body_html": self.description or 'string',
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
            print(response.json()['product'])  # check
            existed_product_haravan = self.env['product.template'].search(
                [('default_code', '=', self.default_code)], limit=1)
            existed_product_haravan.haravan_product_id = response.json()['product'][
                'id']  # chu y ep kieu neu kieu dlu !=string
        else:
            raise ValidationError(_('Create Product Fail in Sync with API Haravan'))
        # except Exception as e:
        #     print(e)

    ## UPDATE
    ###########
    def update_products_haravan_sales(self):
        pass
        # # try:
        # # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
        # token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
        # url = "https://apis.haravan.com/com/products/" + self.seller_product_id + ".json"
        # payload = json.dumps({
        #     "product": {
        #         "body_html": self.description or 'string',
        #         "body_plain": None,
        #         "created_at": None,
        #         "handle": None,
        #         "id": self.seller_product_id,
        #         "images": [
        #             {
        #                 "src": self.image
        #             }
        #         ],
        #         "product_type": self.product_type,
        #         "published_at": None,
        #         "published_scope": None,
        #         "tags": self.tags,
        #         # "template_suffix": "product",
        #         "title": self.name,
        #         "updated_at": None,
        #         "variants": [
        #             {
        #                 "barcode": self.barcode,
        #                 "compare_at_price": 1500,
        #                 "created_at": None,
        #                 "fulfillment_service": None,
        #                 "grams": 550,
        #                 "id": 1040046883,
        #                 "inventory_management": "haravan",
        #                 "inventory_policy": "deny",
        #                 "inventory_quantity": 0,
        #                 "old_inventory_quantity": 0,
        #                 "inventory_quantity_adjustment": None,
        #                 "position": 1,
        #                 "price": 100,
        #                 "product_id": self.seller_product_id,
        #                 "requires_shipping": False,
        #                 "sku": "sku123",
        #                 "taxable": False,
        #                 "title": "Blue / 155",
        #                 "updated_at": None,
        #                 "image_id": None,
        #                 "option1": "Hồng",
        #                 "option2": "M",
        #                 "option3": "Default Title",
        #                 "inventory_advance": None
        #             },
        #             # {
        #             #     "barcode": "qqq",
        #             #     "compare_at_price": 1500,
        #             #     "created_at": "2019-05-31T09:12:00.55Z",
        #             #     "fulfillment_service": null,
        #             #     "grams": 200,
        #             #     "id": 1040046884,
        #             #     "inventory_management": "haravan",
        #             #     "inventory_policy": "continue",
        #             #     "inventory_quantity": 0,
        #             #     "old_inventory_quantity": 0,
        #             #     "inventory_quantity_adjustment": null,
        #             #     "position": 2,
        #             #     "price": 200,
        #             #     "product_id": 1020104002,
        #             #     "requires_shipping": true,
        #             #     "sku": "123",
        #             #     "taxable": false,
        #             #     "title": "Black / 159",
        #             #     "updated_at": "2019-05-31T09:12:00.55Z",
        #             #     "image_id": null,
        #             #     "option1": "Black",
        #             #     "option2": "159",
        #             #     "option3": null,
        #             #     "inventory_advance": null
        #             # }
        #         ],
        #         "vendor": self.vendor,
        #         "options": [
        #             {
        #                 "name": "Color",
        #                 "id": 2448194925,
        #                 "position": 1,
        #                 "product_id": self.seller_product_id
        #             },
        #             {
        #                 "name": "Size",
        #                 "id": 2448194926,
        #                 "position": 2,
        #                 "product_id": self.seller_product_id
        #             },
        #             {
        #                 "name": "Title",
        #                 "id": 2448194927,
        #                 "position": 3,
        #                 "product_id": self.seller_product_id
        #             }
        #         ],
        #         "only_hide_from_list": False,
        #         "not_allow_promotion": False
        #     }
        # })
        # headers = {
        #     # 'Authorization': 'Bearer ' + current_seller.token_connect
        #     'Content-Type': 'application/json',
        #     'Authorization': 'Bearer ' + token_connect
        # }
        # response = requests.request("PUT", url, headers=headers, data=payload)
        # print(response.text)  # check
        # if response.json()['product']:
        #     print(response.json()['product'])
        # else:
        #     raise ValidationError(_('Update Product Fail in Sync with API Haravan'))

        # except Exception as e:
        #     print(e)


    ###### API DELETE 1 PRODUCT FOLLOW ID
    def delete_products_haravan_sales(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products/" + self.haravan_product_id + ".json"
            payload = json.dumps({
                "product": {
                    "id": self.haravan_product_id
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
