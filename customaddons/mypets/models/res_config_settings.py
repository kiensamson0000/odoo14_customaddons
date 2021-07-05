from odoo import api, fields, models

"""
    Tạo mới một settings trong Odoo cho custom addon
    Khi viết 1 custom addon mới, trong trường hợp cần thiết muốn thêm settings cho custom addon
    Tạo trường dữ liệu cho thiết lập: Các settings của Odoo được hiện thực lưu trữ tại model res.config.settings, 
    việc đặt tên field trong model mang ý nghĩa
"""

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_basic_price = fields.Float('Default Pets Basic Price', default_model='my.pet')
    mypets_is_check_duplicated_pet_name = fields.Boolean('Check Duplicated Pet Name', config_parameter='mypets.is_check_duplicated_pet_name')


