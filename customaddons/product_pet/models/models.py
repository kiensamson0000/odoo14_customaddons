# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

# Delegation Inheritance
# Cho phép link record của model mới đến record của model gốc.
# Khi thay đổi value một field ở record của model gốc thì phần thừa kế trong model mới cũng đồng bộ thay đổi theo
# Model mới lưu trữ trên bảng riêng và có view riêng.
# Trong Odoo, thường kế thừa kiểu model product.template và product.product. Hiểu rằng product.template là một template cho product sẽ bán (ví dụ: cây son). Còn product.product sẽ là các variant của product template (ví dụ: cây son màu đỏ, màu xanh, màu hồng, …). Các record trong lớp con sẽ link đến record (cây son) trong lớp cha (gốc).
# Thừa kế cho phép mô tả các biến thể của một sản phẩm. Việc cập nhật thông tin ở My Pet sẽ đồng bộ đến tất cả các Product Pet đang được liên kết đến record bị thay đổi đó.
# Basic_price tăng $120 => Pet mèo biến thể cx được cập nhật giá, ko cần modify từng record variant
# Cách thừa kế phù hợp để thiết kế model trong Odoo rất quan trọng.

class ProductPet(models.Model):
    _name = "product.pet"
    _inherits = {'my.pet': 'my_pet_id'}         #inherit all + cu the 1 field
    _description = "Product Pet"

    my_pet_id = fields.Many2one(
        'my.pet', 'My Pet',                     #
        auto_join=True, index=True, ondelete="cascade", required=True)  #ondelete: 'cascade': xóa cha mất thằng con, 'set default': xóa cha tk con vẫn còn và

    pet_type = fields.Selection([
        ('basic', 'Basic'),
        ('intermediate','Intermediate'),
        ('vip', 'Vip'),
        ('cute', 'Cute'),
    ], string="Pet type",default='basic')        # string (tên hiển thị) , default (mặc định values)

    pet_color = fields.Selection([
        ('white', 'White'),
        ('black', 'Black'),
        ('green','Green'),
        ('yellow','Yellow'),
    ], string="Pet Color",default='white')

    bonus_price = fields.Float("Bonus Price", default=0)

    final_price = fields.Float("Final Price", compute='_compute_final_price')

    def _compute_final_price(self): # hàm tính $$$ mèo cụ thể
        for record in self:
            record.final_price = record.basic_price + record.bonus_price