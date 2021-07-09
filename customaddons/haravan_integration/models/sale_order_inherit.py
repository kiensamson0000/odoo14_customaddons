
from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    _description = "Inherit sale.order"

    haravan_order_id = fields.Char('ID')
        # partner_invoice_id = fields.Char('Invoice Address')
        # validity_date = fields.Char('Expiration')
        # date_order = fields.Char('Quotation Date')
    haravan_financial_status = fields.Char('Financial status')  # trang thai thanh toan
    haravan_gateway = fields.Char('Payment methods')
    # tracking_company = fields.Char('Shipping unit')        #ten nha van chuyen
    haravan_fulfillment_status = fields.Char('Fulfillment status')  # trang thai giao hang
    # haravan_created_at = fields.Char('Create at')     ~~~~ date_order
    haravan_source_name = fields.Char('Sales Channel')
    # haravan_subtotal_price = fields.Float('Amount total')         ~~~~~~~~ amount_total(core)
