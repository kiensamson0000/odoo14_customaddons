# -*- coding: utf-8 -*-
# from odoo import http


# class TestAddon(http.Controller):
#     @http.route('/test_addon/test_addon/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_addon/test_addon/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_addon.listing', {
#             'root': '/test_addon/test_addon',
#             'objects': http.request.env['test_addon.test_addon'].search([]),
#         })

#     @http.route('/test_addon/test_addon/objects/<model("test_addon.test_addon"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_addon.object', {
#             'object': obj
#         })
