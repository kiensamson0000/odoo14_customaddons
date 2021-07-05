# -*- coding: utf-8 -*-

import odoo
import json
import logging
from odoo.addons.mypets.controllers.controllers import MyPetAPI
_logger = logging.getLogger(__name__)

"""
    Để kế thừa controller thực chất thừa kế lớp odoo.http.Controller. Việc thừa kế các built-in controller của Odoo hoặc của một controller trong custom module cho phép "override" phương thức để thay đổi hành vi, hoặc kết quả trả về của controller / api.
    NÊN thừa kế và override phương thức để chỉnh sửa (built-in) module. Không thực hiện sửa code trực tiếp ở module gốc, vì đây có thể gọi là "bad practice" 
"""

class MyPetAPIInherit(MyPetAPI):
    @odoo.http.route()  #ko đặc tả tham số sẽ giữ routing gốc trong controller cha
    def foo_handler(self):
        return "New 'foo' API!"

    @odoo.http.route('/bar2')  #đặc tả ecorator @route(), sẽ override routing gốc.
    def bar_handler(self):
        return json.dumps({
            "content": "New 'bar' API!"
        })

    @odoo.http.route()
    def pet_handler(self, dbname, id, **kw):
        _logger.warning("Pet handler called~")
        result = super(MyPetAPIInherit, self).pet_handler(dbname, id)
        _logger.warning("Post processing~")
        return result

