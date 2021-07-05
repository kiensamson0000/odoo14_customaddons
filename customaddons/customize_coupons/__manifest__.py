# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales order - Customize Coupons',
    'version': '1.1',
    'category': 'Uncategorized',
    'summary': 'Sales internal machinery',
    'description': """
        This module contains all the common features of Sales Management and eCommerce.
    """,
    'author': "ByMrKien",
    'depends': [ #update 'sale' module_name inheritance, default="'sales_team', 'payment', 'portal', 'utm',
        'base',
        'sale_management',
        'website_sale',
    ],

    'data': [
        'security/security.xml',
        'views/sale_order.xml',
        'views/customize_coupons_views.xml',
        'views/code_customer_views.xml',
        'wizard/update_coupons_code.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
