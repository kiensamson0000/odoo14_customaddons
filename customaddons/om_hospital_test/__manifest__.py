# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management',
    'version': '1.0',
    'summary': 'Hospital Management Software',
    'sequence': -100,               # values = âm --> hiển thị đầu tiên App
    'description': """Hospital Management Software""",
    'category': 'Productivity',     # category bao gồm nhiều loại,https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    'website': 'https://www.odoomates.tech',
    'license': 'LGPL-3',            # distribution license for the module, defaults: LGPL-3
    'depends': [
        'sale', 'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/data.xml',
        'views/patient.xml',
        'views/sale_orders.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/appointment.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
