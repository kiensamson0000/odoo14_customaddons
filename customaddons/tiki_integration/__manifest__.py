# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Tiki Integration',
    'version': '1.1',
    'summary': '',
    'sequence': 10,
    'description': """
    Tiki Integration with API by Python Http Request
    """,
    'category': 'Uncategorized',
    'website': '#',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/connect_shop_wizard.xml',
        'views/tiki_seller_product_view.xml',
        'views/tiki_categories_view.xml',
        'views/tiki_seller_view.xml',
        # 'views/assets_backend.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
     #  'qweb': [
     #      'static/src/xml/template.xml',
     # ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
