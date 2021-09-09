import requests
from odoo import fields, models, api


class TikiCategories(models.Model):
    _name = "tiki.categories"
    _description = "Categories"

    category_id = fields.Char('Category ID')
    name = fields.Char('Name')
    status = fields.Char('Status')
    is_primary = fields.Boolean('Primary')
    parent_id = fields.Char('Parent ID')
    parent_ids = fields.Many2one(omodel_name='tiki.categories')

    # seller_id = fields.Many2one('tiki.seller', string='Seller', ondelete='cascade')
    # secret = fields.Char(related='seller_id.secret', string='Secret')
    # user_agent = fields.Text(related='seller_id.user_agent', string='User Agent')

    # url_key = fields.Char('URL Key')
    # path = fields.Char('Path')
    # level = fields.Integer('Level')
    # include_in_menu = fields.Integer('Include in Menu')
    # typical_product = fields.Boolean('Typical Product')
    # is_default = fields.Boolean('Default')
    # position = fields.Integer('Position')
    # is_document_required = fields.Boolean('Document Required')

    # def get_categories_tiki(self):
    #     current_seller = self.env['tiki.seller'].sudo().search([])[0]
    #     url = "https://api-sellercenter.tiki.vn/integration/categories"
    #     payload = {
    #         # 'parent_id' = 'id',
    #     }
    #     headers = {
    #         'tiki-api': current_seller.secret,
    #         'User-Agent': current_seller.user_agent,
    #     }
    #     response = requests.request("GET", url, headers=headers, data=payload)
    #     categories = response.json()
    #     val = {}
    #     if categories:
    #         for cate in categories:
    #             try:
    #                 if ('id' and 'name' and 'status' and 'is_primary') in cate:
    #                     val['category_id'] = cate['id']
    #                     val['name'] = cate['name']
    #                     val['status'] = cate['status']
    #                     val['is_primary'] = cate['is_primary']
    #             except Exception as e:
    #                 print(e)
    #             existed_category = self.env['tiki.categories'].search([('category_id', '=', cate['id'])], limit=1)
    #             if len(existed_category) < 1:
    #                 self.create(val)
    #             else:
    #                 existed_category.write(val)
    #
    #             try:
    #                 url2 = url + '?parent_id=' + str(cate['id'])
    #                 response = requests.request("GET", url2, headers=headers, data=payload)
    #                 parent_categories = response.json()
    #             except Exception as e:
    #                 print(e)

    def get_categories_tiki_recursive(self):
        current_seller = self.env['tiki.seller'].sudo().search([])[0]
        self.parent_id = 1
        url = "https://api-sellercenter.tiki.vn/integration/categories" + "?parent_id=" + str(self.parent_id)
        payload = {
        }
        headers = {
            'tiki-api': current_seller.secret,
            'User-Agent': current_seller.user_agent,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        categories = response.json()

    # # request get url :https://api-sellercenter.tiki.vn/integration/categories => respond data
    # for x in data
    #     x['id']

