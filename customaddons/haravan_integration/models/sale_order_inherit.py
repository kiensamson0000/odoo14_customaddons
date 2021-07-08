
from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    _description = "Inherit sale.order"

    haravan_order_id = fields.Char('ID')
    haravan_name = fields.Char('Customer')
    # partner_invoice_id = fields.Char('Invoice Address')
    haravan_address1 = fields.Char('Delivery Address')
    # validity_date = fields.Char('Expiration')
    # date_order = fields.Char('Quotation Date')
    haravan_financial_status = fields.Char('Financial status')  # trang thai thanh toan
    haravan_gateway = fields.Char('Payment methods')
    # tracking_company = fields.Char('Shipping unit')        #ten nha van chuyen
    haravan_fulfillment_status = fields.Char('Fulfillment status')  # trang thai giao hang
    haravan_created_at = fields.Char('Create at')
    haravan_email = fields.Char('Email')
    haravan_phone = fields.Char('Phone Number')
    haravan_source_name = fields.Char('Sales Channel')
    haravan_subtotal_price = fields.Float('Amount total')
    haravan_list_orders = fields.Text()  # add 1 field save get_data_order of file json

    # product_in_order_sale_order = fields.One2many('sale.order.line', 'product_in_list_order_sale_order')

