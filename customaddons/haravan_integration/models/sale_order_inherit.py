from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    _description = "Inherit sale.order"

    haravan_order_id = fields.Char('ID')
    haravan_gateway = fields.Char('Payment methods')
    haravan_carrier_status_code = fields.Selection([
        ('readytopick','chờ lấy hàng'),
        ('picking','đang đi lấy'),
        ('delivering','đang giao hàng'),
        ('delivered','đã giao hàng'),
        ('cancel','hủy giao hàng'),
        ('return','chuyển hoàn'),
        ('pending','chờ xử lý'),
        ('notmeetcustomer','không gặp khách'),
        ('waitingforreturn','chờ chuyển hoàn'),
    ], string='Carrier Status', store=True)           #trạng thái giao hàng
    haravan_carrier_cod_status_code = fields.Selection([
        ('none','Không'),
        ('codpending','Chưa nhận'),
        ('codpaid',' Chưa nhận'),
        ('codreceipt',' Đã nhận')
    ], string='Carrier Cod Status', store=True)           #trạng thái thu tiền COD
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