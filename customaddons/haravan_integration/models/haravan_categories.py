import requests
import json
from odoo import fields, models, api


class HaravanCategories(models.Model):
    _name = "haravan.categories"
    _description = "API Categories Haravan"

    product_type = fields.Char('Product Type')

    #############################
    ## USE API CATEGORY "HARAVAN INTEGRATION" ON Module "Haravan Integration"
    #############################
    def get_categories_haravan(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/products/types.json"
            payload = {}
            headers = {
                # 'Authorization': 'Bearer ' + current_seller.token_connect
                'Authorization': 'Bearer ' + token_connect
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            result_categories = response.json()
            categories = result_categories["types"]
            val = {}
            if categories:
                for cate in categories:
                    try:
                        val['product_type'] = cate
                    except Exception as e:
                        print(e)
                    existed_cate = self.env['haravan.categories'].search([('product_type', '=', cate)], limit=1)
                    if not existed_cate:
                        self.env['haravan.categories'].create(val)
                    else:
                        existed_cate.write(val)
        except Exception as e:
            print(e)


class ProductCategoriesInherit(models.Model):
    _inherit = "product.category"
    _description = "Inherit product category"

    haravan_product_type = fields.Char('Product Type')

    #############################
    ## USE API CATEGORY "HARAVAN INTEGRATION" on app "Sales"
    #############################
    def get_categories_haravan_sale(self):
        # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
        token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
        url = "https://apis.haravan.com/com/products/types.json"
        payload = {}
        headers = {
            # 'Authorization': 'Bearer ' + current_seller.token_connect
            'Authorization': 'Bearer ' + token_connect
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        result_categories = response.json()
        categories = result_categories["types"]
        val = {}
        if categories:
            for cate in categories:
                try:
                    val['product_type'] = cate
                except Exception as e:
                    print(e)
                existed_cate = self.env['product.category'].search([('haravan_product_type', '=', cate)], limit=1)
                if not existed_cate:
                    self.env['product.category'].sudo().create(val)
                else:
                    existed_cate.write(val)