# -*- coding: utf-8 -*-

"""
    Chứa information cần lưu trữ thuộc tính PET'
"""

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class MyPet(models.Model):
    _name = "my.pet"                   ######
    _description = "My pet model"

    name = fields.Char('Pet Name', required=True)            # modifiers:required = True (values not null)
    nickname = fields.Char(string='Nickname')                       # Name hiển thị nên để string = "Nickname" thay vì  'Nickname'
    description = fields.Text(string='Pet Description')
    basic_price = fields.Float(string='Basic Price', default=0) # su dung trong addon "product_pet"
    age = fields.Integer(string='Pet Age', default=1)
    weight = fields.Float(string='Weight (kg)')
    dob = fields.Date(string='DOB', required=False)         # values can = null
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')
    pet_image = fields.Binary(string="Pet Image", attachment=True, help="Pet Image")    # Binary: save ảnh.       # help: hiển thị text ghi chú
    owner_id = fields.Many2one(comodel_name='res.partner', string='Owner')            # Many2one: quan hệ N-1
    product_ids = fields.Many2many(comodel_name='product.product',                    # Many2many: quan hệ N-N, tạo 1 bảng tạm lưu trữ (column 1, column2,...)
                                string="Related Products",
                                relation='pet_product_rel',
                                column1='col_pet_id',
                                column2='col_product_id')


    # thực hiện logic ở backend, button tree gọi đến:
    def cus_remove_button(self):
        for pet in self:
            pet.unlink()
        # _logger.warning(self.id) # [5]
        # _logger.warning(self.ids) # [5]
        pass

    @api.model
    def create(self, vals):
        is_check_duplicated_pet_name = self.env['ir.config_parameter'].sudo().get_param('mypets.is_check_duplicated_pet_name', default=False)
        if is_check_duplicated_pet_name:
            vals = [vals,] if not isinstance(vals, (tuple, list)) else vals  # isinstance: kiểm tra 1 đối tượng (object, classinfo), classinfo: class, type, hoặc tuple. KQ: True/False
            for val in vals:
                pet_name = val['name']
                pet_record = self.search([('name','=', pet_name)])
                if pet_record:
                    raise ValidationError(_("Duplicated pet name @ %s" % pet_name))
        return super(MyPet, self).create(vals)


    # Them phuong thuc sau vao model:
#   Đây chính là lỗi do phương thức btn_multi_update chưa được hiện thực ở backend (model my.pet).
#   Ở bước này tự code "business logic" theo yêu cầu của khách hàng / người dùng.
#   Code 1 action đơn giản minh họa (là Batch Update wizard)

#   Khi điền giá trị vào form => "Confirm" => reload lại dữ liêu thay đổi

    @api.model
    def btn_multi_update(self):
        # we can do something on records... it's up to you!
        # res = { 'type': 'ir.actions.client', 'tag': 'reload' } # reload the current page/url
        active_ids = [pet.id for pet in self.env["my.pet"].search([])]
        res = {
            "name": _("Multi Update"),
            "type": "ir.actions.act_window",
            "res_model": "batch.update.wizard",
            "binding_model_id": self.env['ir.model']._get("my.pet").id,
            "view_mode": "form",
            "target": "new",
            "views": [[False, 'form']],
            "context": {
                "active_ids": active_ids,
                "default_dob": fields.Date.context_today(self),
                "default_owner_id": self.env.user.partner_id.id,
            },
        }
        return res