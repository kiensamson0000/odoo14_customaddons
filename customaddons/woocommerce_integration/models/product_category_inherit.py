from odoo import fields, models, api, _
import requests
import json
from odoo.exceptions import UserError, ValidationError


#       Class Inherit Product Category
class ApiWoocommerceProductCategoryInherit(models.Model):
    _inherit = "product.category"

    woocommerce_cate_id = fields.Integer(string='Category ID')
    woocommerce_parent_id = fields.Char(string='Woocommerce Parent ID')

    #       Add To Module Sale
    def get_categories_woocommerce(self):
        try:
            current_seller = self.env['woocommerce.seller'].sudo().search([])[0]

            url = str(current_seller.link_website) + "wp-json/wc/v3/products/categories?consumer_key=" + str(
                current_seller.consumer_key) + "&consumer_secret=" + str(current_seller.consumer_secret)

            payload = {}
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            result_category = response.json()
            val = {}
            if result_category:
                for cate in result_category:
                    if cate['id']:
                        val['woocommerce_cate_id'] = cate['id']
                        val['name'] = cate['name']
                        val['woocommerce_parent_id'] = cate['parent']
                        val['parent_id'] = None

                        existed_category = self.env['product.category'].search([('woocommerce_cate_id', '=', cate['id'])],
                                                                           limit=1)
                        if len(existed_category) < 1:
                            self.env['product.category'].create(val)
                        else:
                            existed_category.write(val)
                    else:
                        pass
            else:
                raise ValidationError(_('Sync Category From Woocommerce Is Fail.'))
        except Exception as e:
            raise ValidationError(str(e))

