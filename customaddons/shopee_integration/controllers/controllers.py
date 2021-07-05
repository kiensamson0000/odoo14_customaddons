# -*- coding: utf-8 -*-
# from odoo import http


# class ShopeeIntegration(http.Controller):
#     @http.route('/shopee_integration/shopee_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shopee_integration/shopee_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shopee_integration.listing', {
#             'root': '/shopee_integration/shopee_integration',
#             'objects': http.request.env['shopee_integration.shopee_integration'].search([]),
#         })

#     @http.route('/shopee_integration/shopee_integration/objects/<model("shopee_integration.shopee_integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shopee_integration.object', {
#             'object': obj
#         })
