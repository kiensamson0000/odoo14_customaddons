import requests
import json
from datetime import *

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError


class HaravanSellerOrders(models.Model):
    _name = 'haravan.seller.orders'
    _description = 'API Order Haravan'

    id_customer = fields.Char('Customer ID')
    order_id = fields.Char('Order ID')
    name = fields.Char('Customer')
    # partner_invoice_id = fields.Char('Invoice Address')
    address1 = fields.Char('Delivery Address')
    # validity_date = fields.Char('Expiration')
    # date_order = fields.Char('Quotation Date')
    financial_status = fields.Char('Financial status')  # trang thai thanh toan
    gateway = fields.Char('Payment methods')
    # tracking_company = fields.Char('Shipping unit')        #ten nha van chuyen
    fulfillment_status = fields.Char('Fulfillment status')  # trang thai giao hang
    created_at = fields.Char('Create at')
    email = fields.Char('Email')
    phone = fields.Char('Phone Number')
    source_name = fields.Char('Sales Channel')
    subtotal_price = fields.Float('Amount total')
    list_orders = fields.Text()  # add 1 field save get_data_order of file json
    ##############
    order_line = fields.One2many('product.order.haravan', 'product_in_list_order', string='Order Lines')

    @api.constrains('subtotal_price')
    def _check_subtotal_price(self):
        for rec in self:
            if rec.subtotal_price <= 0:
                raise ValidationError(_("Subtotal Price need more than 0 (>0)."))

    #############################
    ## USE API ORDER ON Module "Haravan Integration"
    def get_orders_haravan(self):
        try:
            # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
            token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
            url = "https://apis.haravan.com/com/orders.json"
            payload = {}
            headers = {
                # 'Authorization': 'Bearer ' + current_seller.token_connect
                'Authorization': 'Bearer ' + token_connect
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            result_order = response.json()
            list_orders = result_order['orders']
            val = {}
            list_product = []
            for order in list_orders:
                if 'id' in order:
                    val['order_id'] = order['id']
                    val['name'] = order['billing_address']['name']
                    val['address1'] = order['billing_address']['address1']
                    val['email'] = order['email']
                    val['phone'] = order['billing_address']['phone']
                    val['created_at'] = order['created_at']
                    val['source_name'] = order['source_name']
                    val['subtotal_price'] = order['subtotal_price']
                    val['financial_status'] = order['financial_status']
                    val['gateway'] = order['gateway']
                    # val['tracking_company'] = order['fulfillments']['tracking_company']
                    val['fulfillment_status'] = order['fulfillment_status']
                    existed_order = self.env["haravan.seller.orders"].sudo().search([('order_id', '=', order['id'])],
                                                                                    limit=1)
                    if not existed_order:
                        new_record = self.env["haravan.seller.orders"].create(val)
                        if new_record:
                            if order['line_items']:
                                val_product = order['line_items']
                                for product in val_product:
                                    if 'id' in product:
                                        list_product.append({
                                            'product_id': product['variant_id'],
                                            'name': product['name'],
                                            'sku': product['sku'],
                                            'quantity': product['quantity'],
                                            'vendor': product['vendor'],
                                            'price': product['price'],
                                            'type': product['type']
                                        })
                                        if list_product:
                                            new_record.order_line = [(0, 0, e) for e in list_product]
                                        list_product = []
                    else:
                        existed_order.sudo().write(val)
                        # existed_order.env['haravan.seller.orders'].sudo().write(val)
        except Exception as e:
            print(e)

    ### CREATE
    ################
    # def create_orders_haravan(self):
    #     # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
    #     infor_product_order = self.env['product.order.haravan'].sudo().search([])[0]
    #
    #     token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
    #     url = "https://apis.haravan.com/com/orders.json"
    #     # name (check tên của customer đúng format(họ đệm & tên))
    #     payload = json.dumps({
    #         "order": {
    #             "billing_address": {
    #                 "address1": self.address1,
    #                 "phone": self.phone,
    #                 "name": self.name
    #             },
    #             "email": self.email,
    #             "source_name": self.source_name,
    #             "fulfillment_status": self.fulfillment_status,
    #             "line_items": [
    #                 {
    #                     "variant_id": 44765421323529,
    #                     "quantity": 1111121
    #                 }]
    #         }
    #     })
    #     headers = {
    #         # 'Authorization': 'Bearer ' + current_seller.token_connect
    #         'Content-Type': 'application/json',
    #         'Authorization': 'Bearer ' + token_connect
    #     }
    #     response = requests.request("POST", url, headers=headers, data=payload)
    #     print(response.text)  # check
    #     if response.json()['order']:
    #         print(response.json()['order'])
    #         self.order_id = response.json()['order']['id']  # save order_id on database
    #     else:
    #         raise ValidationError(_('Create Product Fail in Sync with API Haravan'))

    #############################
    ## USE API ORDER ON APP "SALE"
    def get_orders_haravan_sale(self):
        # try:
        # current_seller = self.env['haravan.seller'].sudo().search([])[0]    (chua connect duoc)
        token_connect = '914CE4F424C6DCD6EC3E50792E040C11348E8E27E5C73B5E8A2BB9F3C9690FFB'
        url = "https://apis.haravan.com/com/orders.json"
        payload = {}
        headers = {
            # 'Authorization': 'Bearer ' + current_seller.token_connect
            'Authorization': 'Bearer ' + token_connect
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        result_order = response.json()
        list_orders = [result_order['orders'][2]]
        # list_orders = result_order['orders']
        val = {}
        list_product = []
        val_customer = {}
        for order in list_orders:
            try:
                if 'id' in order:
                    # get information customer = api order
                    # val_customer['parent_id'] = order['billing_address']['id']
                    val_customer['name'] = order['billing_address']['name']
                    val_customer['street'] = order['billing_address']['address1']
                    val_customer['email'] = order['email']
                    val_customer['phone'] = order['billing_address']['phone']
                    # val_customer['tags'] = order['tags']
                    existsed_customer = self.env['res.partner'].sudo().search(
                        ['&', ('phone', '=', order['billing_address']['phone']),
                         ('street', '=', order['billing_address']['address1'])], limit=1)
                    if not existsed_customer:
                        self.env['res.partner'].sudo().create(val_customer)
                        ## get information order
                        # field existed (sale.order)
                        val['amount_total'] = order['subtotal_price']
                        val['name'] = order['id']
                        # val['amount_untaxed'] = order['sub_total']
                        ### val['date_order'] = datetime.fromtimestamp(order['created_at'])
                        val['partner_id'] = existsed_customer.id
                        # val['tracking_company'] = order['fulfillments']['tracking_company']
                        # new add field (sale.order)
                        val['haravan_order_id'] = order['id']
                        val['haravan_source_name'] = order['source_name']
                        val['haravan_financial_status'] = order['financial_status']
                        val['haravan_gateway'] = order['gateway']
                        val['haravan_fulfillment_status'] = order['fulfillment_status']
                        existed_order = self.env['sale.order'].sudo().search([('haravan_order_id', '=', order['id'])],
                                                                             limit=1)
                        if not existed_order:
                            new_record = self.env['sale.order'].create(val)
                            if new_record:
                                if order['line_items']:
                                    val_product = order['line_items']
                                    for product in val_product:
                                        try:
                                            if 'id' in product:
                                                existed_product_haravan = self.env['product.template'].sudo().search(
                                                    [('default_code', '=', product['product_id'])], limit=1)
                                                list_product.append({
                                                    'product_id': existed_product_haravan.product_variant_id.id,
                                                    'product_uom_qty': product['quantity'],
                                                    'price_unit': product['price']
                                                })
                                                if list_product:
                                                    new_record.order_line = [(0, 0, e) for e in list_product]
                                                list_product = []
                                        except Exception as e:
                                            print(e)
                        else:
                            existed_order.sudo().write(val)
                    else:
                        self.env['res.partner'].sudo().write(val_customer)
                        ## get information order
                        # field existed (sale.order)
                        val['amount_total'] = order['subtotal_price']
                        # val['amount_untaxed'] = order['sub_total']
                        ##### val['date_order'] = datetime.fromtimestamp(order['created_at'])
                        val['name'] = order['id']
                        val['partner_id'] = existsed_customer.id
                        # val['tracking_company'] = order['fulfillments']['tracking_company']
                        # new add field (sale.order)
                        val['haravan_order_id'] = order['id']
                        val['haravan_source_name'] = order['source_name']
                        val['haravan_financial_status'] = order['financial_status']
                        val['haravan_gateway'] = order['gateway']
                        val['haravan_fulfillment_status'] = order['fulfillment_status']
                        # In sale.order khong co field order_id => create new field haravan_order_id
                        existed_order = self.env['sale.order'].sudo().search(
                            [('haravan_order_id', '=', str(order['id']))],
                            limit=1)
                        if not existed_order:
                            new_record = self.env['sale.order'].create(val)
                            if new_record:
                                if order['line_items']:
                                    val_product = order['line_items']
                                    list_product = []
                                    for product in val_product:
                                        try:
                                            if 'id' in product:
                                                existed_product_haravan = self.env['product.template'].sudo().search(
                                                    [('default_code', '=', product['product_id'])], limit=1)
                                                list_product.append({
                                                    'product_id': existed_product_haravan.product_variant_id.id,
                                                    'product_uom_qty': product['quantity'],
                                                    'price_unit': product['price'],
                                                })
                                        except Exception as e:
                                            print(e)
                                    if len(list_product) > 0:
                                        new_record.order_line = [(0, 0, e) for e in list_product]
                        else:
                            existed_order.sudo().write(val)
            except Exception as e:
                print(e)


class ProductOrderHaravan(models.Model):
    _name = "product.order.haravan"
    _description = "Information product follow order"

    product_id = fields.Char(string='Product ID')
    name = fields.Char(string='Product')
    sku = fields.Char(string='SKU')
    quantity = fields.Integer()
    price = fields.Float()
    vendor = fields.Char()
    type = fields.Char()
    ###########
    product_in_list_order = fields.Many2one('haravan.seller.orders', string="Appointment")
