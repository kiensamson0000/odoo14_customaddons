# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contract Management',
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
        'wizard/create_contract_wizard.xml',
        'views/sale_order.xml',
        'views/res_partner_inherit_view.xml',
        'views/contract_management_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'installable': True,
}
