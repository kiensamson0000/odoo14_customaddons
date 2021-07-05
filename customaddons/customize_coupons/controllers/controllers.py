# -*- coding: utf-8 -*-
# from odoo import http


# class CustomizeCoupons(http.Controller):
#     @http.route('/customize_coupons/customize_coupons/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customize_coupons/customize_coupons/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customize_coupons.listing', {
#             'root': '/customize_coupons/customize_coupons',
#             'objects': http.request.env['customize_coupons.customize_coupons'].search([]),
#         })

#     @http.route('/customize_coupons/customize_coupons/objects/<model("customize_coupons.customize_coupons"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customize_coupons.object', {
#             'object': obj
#         })
