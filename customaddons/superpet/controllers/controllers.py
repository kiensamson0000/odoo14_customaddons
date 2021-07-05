# -*- coding: utf-8 -*-
# from odoo import http


# class Superpet(http.Controller):
#     @http.route('/superpet/superpet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/superpet/superpet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('superpet.listing', {
#             'root': '/superpet/superpet',
#             'objects': http.request.env['superpet.superpet'].search([]),
#         })

#     @http.route('/superpet/superpet/objects/<model("superpet.superpet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('superpet.object', {
#             'object': obj
#         })
