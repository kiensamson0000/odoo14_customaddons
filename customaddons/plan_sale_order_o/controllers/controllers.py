# -*- coding: utf-8 -*-
# from odoo import http


# class PlanSaleOrderO(http.Controller):
#     @http.route('/plan_sale_order_o/plan_sale_order_o/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/plan_sale_order_o/plan_sale_order_o/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('plan_sale_order_o.listing', {
#             'root': '/plan_sale_order_o/plan_sale_order_o',
#             'objects': http.request.env['plan_sale_order_o.plan_sale_order_o'].search([]),
#         })

#     @http.route('/plan_sale_order_o/plan_sale_order_o/objects/<model("plan_sale_order_o.plan_sale_order_o"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('plan_sale_order_o.object', {
#             'object': obj
#         })
