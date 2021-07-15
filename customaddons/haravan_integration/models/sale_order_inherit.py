import requests
import json
from datetime import *

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    _description = "Inherit sale.order"

    haravan_order_id = fields.Char('ID')
    haravan_gateway = fields.Char('Payment methods')
    haravan_carrier_status_code = fields.Selection([
        ('readytopick', 'chờ lấy hàng'),
        ('picking', 'đang đi lấy'),
        ('delivering', 'đang giao hàng'),
        ('delivered', 'đã giao hàng'),
        ('cancel', 'hủy giao hàng'),
        ('return', 'chuyển hoàn'),
        ('pending', 'chờ xử lý'),
        ('notmeetcustomer', 'không gặp khách'),
        ('waitingforreturn', 'chờ chuyển hoàn')
    ], string='Carrier Status')  # trạng thái giao hàng
    haravan_carrier_cod_status_code = fields.Selection([
        ('none', 'Không'),
        ('codpending', 'Chưa nhận'),
        ('codpaid', ' Chưa nhận'),
        ('codreceipt', ' Đã nhận')
    ], string='Carrier Cod Status')  # trạng thái thu tiền COD
    haravan_source_name = fields.Char('Sales Channel')
    # haravan_financial_status = fields.Selection([
    #     ('pending', 'Chưa thanh toán'),
    #     ('partially_paid', 'Đã thanh toán một phần'),
    #     ('paid', 'Đã thanh toán'),
    #     ('partiallyrefunded', 'Đã thanh toán một phần'),
    #     ('refunded', 'Đã hoàn tiền'),
    #     ('voided', 'Đã huỷ')
    # ], string='Financial status', store=True)
    # tracking_company = fields.Char('Shipping unit')        #ten nha van chuyen
    # haravan_fulfillment_status = fields.Selection([
    #     ('not_fulfilled', 'Chưa hoàn thành'),
    #     ('partial', 'Hoàn thành một phần'),
    #     ('fulfilled', 'Đã hoàn thành')
    # ],string='Fulfillment status')  # trạng thái tạo vận đơn
    # haravan_subtotal_price = fields.Float('Amount total')  #Tổng giá đơn hàng    ~~~~~~~~ amount_total(core)
    # total_discounts (number) Tổng giá trị khuyến mãi của đơn hàng
    # haravan_created_at = fields.Char('Create at')     ~~~~ date_order
    # partner_invoice_id = fields.Char('Invoice Address')
    # validity_date = fields.Char('Expiration')
    # date_order = fields.Char('Quotation Date')
    # haravan_financial_status = fields.Char('Financial status')  # trang thai thanh toan

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
        # list_orders = [result_order['orders'][7]]
        list_orders = result_order["orders"]
        val = {}
        list_product = []
        val_customer = {}
        for order in list_orders:
            try:
                if 'id' in order:
                    ## get infor customer
                    # val_customer['parent_id'] = order['billing_address']['id']
                    val_customer['name'] = order['billing_address']['name']
                    val_customer['street'] = order['billing_address']['address1']
                    val_customer['email'] = order['email']
                    val_customer['phone'] = order['billing_address']['phone']
                    val_customer['mobile'] = order['billing_address']['phone']
                    val_customer['type'] = 'contact'
                    val_customer['check_partner_haravan'] = True
                    # val_customer['comment'] = 'Sync By Call Sendo API'
                    # val_customer['company_type'] = 'person'
                    # val_customer['tags'] = order['tags']
                    existsed_customer = self.env['res.partner'].sudo().search(
                        ['&', ('phone', '=', order['billing_address']['phone']),
                         ('street', '=', order['billing_address']['address1'])], limit=1)
                    if not existsed_customer:
                        self.env['res.partner'].sudo().create(val_customer)
                        ## get infor order
                        val['haravan_order_id'] = order['id']
                        val['name'] = order['id']
                        val['haravan_source_name'] = order['source_name']
                        val['haravan_carrier_status_code'] = str(order['fulfillments']['carrier_status_code'])
                        val['haravan_gateway'] = order['gateway']
                        val['haravan_carrier_cod_status_code'] = order['fulfillments']['carrier_cod_status_code']
                        val['amount_total'] = order['subtotal_price']
                        val['date_order'] = datetime.fromtimestamp(order['created_at'])
                        val['amount_total'] = order['subtotal_price']
                        val['partner_id'] = existsed_customer.id
                        # val['amount_untaxed'] = order['sub_total']
                        existed_order = self.env['sale.order'].sudo().search([('haravan_order_id', '=', order['id'])],
                                                                             limit=1)
                        if not existed_order:
                            new_record = self.env['sale.order'].create(val)
                            if new_record:
                                if 'line_items' in order:
                                    val_product = order['line_items']
                                    for product in val_product:
                                        # try, catch xử lý trường hợp sản phẩm đã xóa nhg vẫn tồn tại trg 1 đơn hàng
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
                        # existsed_customer.sudo().write(val_customer)
                        ## get infor order
                        val['haravan_order_id'] = order['id']
                        val['name'] = order['id']
                        val['haravan_source_name'] = order['source_name']
                        val['haravan_carrier_status_code'] = order['fulfillments']['carrier_status_code']
                        val['haravan_gateway'] = order['gateway']
                        val['haravan_carrier_cod_status_code'] = order['fulfillments']['carrier_cod_status_code']
                        val['amount_total'] = order['subtotal_price']
                        val['date_order'] = datetime.fromtimestamp(order['created_at'])
                        val['amount_total'] = order['subtotal_price']
                        val['partner_id'] = existsed_customer.id
                        # val['amount_untaxed'] = order['sub_total']
                        # In sale.order khong co field order_id => create new field haravan_order_id
                        existed_order = self.env['sale.order'].sudo().search([('haravan_order_id', '=', order['id'])],
                                                                             limit=1)
                        if not existed_order:
                            new_record = self.env['sale.order'].create(val)
                            if new_record:
                                if 'line_items' in order:
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
                                                    'price_unit': product['price']
                                                })
                                        except Exception as e:
                                            print(e)
                                    if len(list_product) > 0:
                                        new_record.order_line = [(0, 0, e) for e in list_product]
                        else:
                            existed_order.sudo().write(val)
            except Exception as e:
                print(e)