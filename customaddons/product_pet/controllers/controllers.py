# -*- coding: utf-8 -*-
# from odoo import http


# class ProductPet(http.Controller):
#     @http.route('/product_pet/product_pet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_pet/product_pet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_pet.listing', {
#             'root': '/product_pet/product_pet',
#             'objects': http.request.env['product_pet.product_pet'].search([]),
#         })

#     @http.route('/product_pet/product_pet/objects/<model("product_pet.product_pet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_pet.object', {
#             'object': obj
#         })
