from odoo import fields, models, api

class ProductCategoriesInherit(models.Model):
    _inherit = "product.category"
    _description = "Inherit product category"

    # haravan_product_cate = fields.Char()
    check_cate_haravan = fields.Boolean('check cate haravan')
