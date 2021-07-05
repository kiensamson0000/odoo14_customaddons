# -*- coding: utf-8 -*-

import odoo
import json
import logging
_logger = logging.getLogger(__name__)   #

class MyPetAPI(odoo.http.Controller):
    # Routing đường dẫn đến route @ /foo -> foo_handler(). Trong hàm foo trả về chuỗi chào mừng.
    @odoo.http.route('/foo', auth='public')  # auth = 'public' trả về dù có login hay ko? Normal auth= 'user'
    def foo_handler(self):
        return "Welcome to 'foo' API!"

    # Viết một bar API trả về dữ liệu dạng chuỗi json, để client có thể parse và xử lý ở frontend.
    @odoo.http.route('/bar', auth='public')
    def bar_handler(self):
        return json.dumps({
            "content": "Welcome to 'bar' API!"
        })

    """
    Tạo một public API trả về thông tin của Pet. Như vậy controller phải đón nhận routing dạng /pet/<DBNAME>/<ID>, 
    sau đó truy vấn model theo database name đọc ra dữ liệu và trả về chuỗi json """

    @odoo.http.route(['/pet/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def pet_handler(self, dbname, id, **kw):
        model_name = "my.pet"
        try:
            registry = odoo.modules.registry.Registry(dbname)    # kết nối đến bảng "my.pet" bằng account admin odoo.SUPERUSER_ID để tìm kiếm và đọc ra dữ liệu
            with odoo.api.Environment.manage(), registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)  # tìm kiếm
                response = {                                                    # đọc dữ liệu
                    "status": "ok",
                    "content": {
                        "name": rec.name,
                        "nickname": rec.nickname,
                        "description": rec.description,
                        "age": rec.age,
                        "weight": rec.weight,
                        "dob": rec.dob.strftime('%d/%m/%Y'),  # Dữ liệu trả về sẽ bị lỗi nếu có Object trong đó, ví dụ trường rec.dob (ngày sinh pet's), sẽ là DateTime object --> phải chuyển sang dạng string tránh lỗi
                        "gender": rec.gender,
                    }
                }
        except Exception:              # Gặp error --> except, trả về response ko exist
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)

    #   truy vấn test theo curl http://localhost:8069/pet/test_db/1