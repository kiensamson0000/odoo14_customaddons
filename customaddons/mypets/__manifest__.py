# -*- coding: utf-8 -*-

# Descriptions information PET'S

{
    'name': "My pet - kienkh.info",
    'summary': """My pet model""",
    'description': """Managing pet information""",
    'author': "kienkh.info",
    'website': "https://thepet.vn/",
    'category': 'Uncategorized',     # Loại module, danh sách category
    'version': '0.1',
    'depends': [                     # dependcy của module sẽ phụ thuộc vào những app / module khác nào. Đặc tả "product" là một module built-in của Odoo. Do đó, khi cài đặt module my_pet sẽ trigger cài đặt app product.
        'product',
    ],
    'data': [                        # liên quan đến view, các file xml
        'security/ir.model.access.csv',
        'wizard/update_order_state_view.xml',
        'views/views.xml',                # <-- DECLARE OUR NEW XML FILE
        'views/res_config_settings_views.xml', # add this
        'views/templates.xml',
    ],
    'qweb': [
        #'static/src/xml/*.xml',
        'static/src/xml/btn_tree_multi_update.xml', # <-- khai bao thua ke qweb vua hien thuc
    ],
    'installable': True,    # True install được
    'application': True,    # Menu Apps, mặc định filter "Apps" được dùng. Nếu application set = False thì không hiện ra khi có filter "Apps", ngược lại Set = True xem như một Application
}