# -*- coding: utf-8 -*-
# from odoo import http


# class HaravanIntegration(http.Controller):
#     @http.route('/haravan_integration/haravan_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/haravan_integration/haravan_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('haravan_integration.listing', {
#             'root': '/haravan_integration/haravan_integration',
#             'objects': http.request.env['haravan_integration.haravan_integration'].search([]),
#         })

#     @http.route('/haravan_integration/haravan_integration/objects/<model("haravan_integration.haravan_integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('haravan_integration.object', {
#             'object': obj
#         })
