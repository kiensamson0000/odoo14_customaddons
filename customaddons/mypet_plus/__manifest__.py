# -*- coding: utf-8 -*-
{
    'name': "My pet (+) - minhng.info",
    'summary': """My pet plus""",
    'description': """Managing pet information""",
    'author': "minhng.info",
    'website': "https://minhng.info",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [           # do kế thừa từ 'mypet'
        'mypets',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_views.xml',
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}