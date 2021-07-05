# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

"""
    Để customize (hoặc thêm mới) được thành phần trong Odoo, phải biết thành phần đó nằm ở đâu, cách tạo mới như nào. 
    Wizard ? dùng khi nào? Câu trả lời: khi cần xử lý trên nhiều record dữ liệu (nhiều hàng trong bảng / model) cùng lúc, để thao tác như: cập nhật hàng lọat, kết xuất báo cáo, … 
    Wizard trong Odoo, customization phổ biến là tạo mới một wizard đặc thù business. Cách tạo & cấu trúc 1 wizard:
        Model: hiện thực transient model (form pop-up)
        View: hiện thực action (act_window) để hiện thị form pop-up
    Cụ thể tạo 1 wizard là update field cho nhiều record thú cưng một lúc, tức multiple update thay vì sửa từng dòng record, values field update sẽ giống nhau hàng lọat.

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

"""

# Model: hiện thực transient model "bay hơi" (form pop-up)

import logging
_logger = logging.getLogger(__name__)


class BatchUpdateWizard(models.TransientModel):
    _name = "batch.update.wizard"  # quy uoc đặt tên trùng với class, tên file .py và .xml
    _description = "Batch update for my.pet model"

    dob = fields.Date('DOB', required=False, default=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default=False)
    owner_id = fields.Many2one('res.partner', string='Owner', default=False)
    basic_price = fields.Float('Basic Price', default=0)

    def multi_update(self):
        ids = self.env.context['active_ids']  # selected ids cac record trong my.pet truyen vao context
        my_pets = self.env["my.pet"].browse(ids) #
        new_data = {}
        if self.dob:
            new_data["dob"] = self.dob
        if self.gender:
            new_data["gender"] = self.gender
        if self.owner_id:
            new_data["owner_id"] = self.owner_id
        if self.basic_price > 0:
            new_data["basic_price"] = self.basic_price

        my_pets.write(new_data)
