import requests

from odoo import fields, models, api


class TikiSellerProduct(models.Model):
    _name = "tiki.seller.product"
    _description = "Seller Product"

    seller_product_id = fields.Char('Product ID')
    sku = fields.Char('SKU')
    name = fields.Char('Product Name')
    master_id = fields.Char('Master ID', nullable=True)
    super_id = fields.Char('Super ID')
    min_code = fields.Char('Min Code')
    seller_product_code = fields.Char('Seller Product Code')
    productset_id = fields.Integer('Product Set ID')
    status = fields.Integer('Status')
    price = fields.Float('Price')
    thumbnail = fields.Char('Thumbnail')
    categories = fields.Many2many(comodel_name='tiki.categories', string='Product Categories')

    def get_seller_product_tiki(self):
        current_seller = self.env['tiki.seller'].sudo().search([])[0]
        url = "https://api-sellercenter.tiki.vn/integration/seller/products"
        payload = {}
        headers = {
            'tiki-api': current_seller.secret,
            'User-Agent': current_seller.user_agent,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        seller_products = response.json()
        list_products = seller_products['data']
        # list_categories = list_products['categories']
        for i in list_products:
            categories = i['categories']
            for k in categories:
                category_id = k['id']
                print(category_id)
        val = {}

        for product in list_products:
            if 'id' in product:
                try:
                    val['seller_product_id'] = product['id']
                    val['name'] = product['name']
                    val['sku'] = product['status']
                    val['master_id'] = product['master_id']
                    val['super_id'] = product['super_id']
                    val['min_code'] = product['min_code']
                    val['seller_product_code'] = product['seller_product_code']
                    val['productset_id'] = product['productset_id']
                    val['status'] = product['status']
                    val['price'] = product['price']
                    val['thumbnail'] = product['thumbnail']
                    # val['categories'] = product['categories.id']
                except Exception as e:
                    print(e)
            existed_seller_product = self.env['tiki.seller.product'].search([('seller_product_id', '=', product['id'])], limit=1)
            if len(existed_seller_product) < 1:
                self.create(val)
            else:
                existed_seller_product.write(val)