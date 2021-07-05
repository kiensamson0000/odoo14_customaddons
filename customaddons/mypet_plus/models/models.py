# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

# Traditional Inheritance (Kế thừa truyền thống)
# Class Inheritance: thêm các thuộc tính mới vào model cũ, hoặc chỉnh sửa các trường thuộc tính cũ. View của model thừa kế và model gốc là dùng chung.
# NOTE: Do kế thừa nên addon mypet_plus vẫn chung form với addon mypet (cha)
# Used thường xuyên customizations module

class MyPetPLus(models.Model):
    _inherit = "my.pet"
    _description = "Extend mypet model"

    #add new field

    toy = fields.Char('Pet Toy', required=False)

    #modify old field

    age = fields.Integer('Pet Age', default=2)      #change default age from 1 to 2

    gender = fields.Selection(selection_add=[('sterilization', 'Sterilization')])     #add one more selection on field gender da khai bao





