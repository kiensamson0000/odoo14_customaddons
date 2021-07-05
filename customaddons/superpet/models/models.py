# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

# Traditional Inheritance (Kế thừa truyền thống)
# Thừa kế Prototype: cho phép clone một model và thêm các thuộc tính mới. Model mới độc lập model cũ do Database bên dưới lưu ở hai bảng khác nhau. Thừa kế không làm ảnh hưởng các field trong view cũ. Cần tạo View mới tương ứng model mới để hiển thị.
# Các record của super.pet và my.pet được lưu trữ độc lập. Khi tạo mới record bên này sẽ không liên quan hay ảnh hưởng bên kia. Đơn giản Super Pet là model nâng cấp mở rộng của My Pet.

class SuperPet(models.Model):
    _name = "super.pet"  # <- new model name
    _inherit = "my.pet"  # <- inherit fields and methods from model "my.pet"
    _description = "Prototype inheritance"

    # add new field
    is_super_strength = fields.Boolean("Is Super Strength", default=False)
    is_fly = fields.Boolean(string="Is Pet Fly",default=False) # nên để string ="Is Fly" thay vì bỏ string như dòng trên
    planet = fields.Char("Planet")

    # avoid error: TypeError: Many2many fields super.pet.product_ids and my.pet.product_ids use the same table and columns
    product_ids = fields.Many2many(comodel_name='product.product',
                                   string="Related Products",
                                   relation='super_pet_product_rel',  # <- change this relation name!
                                   column1='col_pet_id',
                                   column2='col_product_id')