# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Plan Sale Order',
    'version': '1.0',
    'category': 'Sales/Sales',
    'sequence': 8,
    'summary': 'Create and validate plan of sale orders',
    'description': """
Create and validate plan of sale orders
    """,
    'depends': ['mail', 'sale', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_plan.xml',
        'views/sale_order.xml',
        'views/plan_sale_order.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'installable': True,
}
