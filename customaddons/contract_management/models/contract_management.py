from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import *

class ContractManagement(models.Model):
    _name = "contract.management"
    _description = "Contract Management"
    _rec_name = 'order_source'

    contract_id = fields.Char('Mã hợp đồng', required='True', readonly=True, default=lambda self: _('New'))
    contract_type = fields.Selection([
        ('hopdonghthietke', 'Hợp đồng thiết kế'),
        ('hopdongmuaban','Hợp đồng mua bán')
    ], string='Loại hợp đồng', default='hopdonghthietke')
    contract_number = fields.Selection([
        ('stk0123/hdnvs','STK0123HĐNVS'),
        ('mb98123/hdmb522','MB98123/HĐMB522'),
    ], string='Hợp đồng khung', default='stk0123/hdnvs')
    infor_contract = fields.Char('Thông tin hợp đồng')
    contract_sign_date = fields.Date('Ngày ký hợp đồng', default=date.today())
    customer_id = fields.Many2one('res.partner', string='Customer ID', readonly=True, ondelete='cascade')
    cccd_id = fields.Char('Số CCCD')
    date_created = fields.Char('Ngày cấp')
    place = fields.Char('Nơi cấp')
    signer = fields.Char('Người ký')
    order_source = fields.Many2one('sale.order', string='Sale order', readonly=True, ondelete='cascade')
    signer_position = fields.Selection([
        ('giamdoc','Giám đốc'),
        ('truongphong','Trưởng phòng'),
        ('ketoan','Kế toán'),
    ], string='Chức vụ', readonly=True, default='giamdoc')
    contract_address = fields.Char('Địa chỉ hợp đồng')
    contract_construction_date = fields.Datetime('Ngày thi công hợp đồng')
    delivery_address = fields.Char('Địa chỉ giao hàng')
    contract_end_date = fields.Datetime('Ngày kết thúc hợp đồng')
    category_contract = fields.Selection([
        ('dautu','Đầu tư'),
        ('suachua','Sửa chữa'),
    ], string='Hạng mục hợp đồng', readonly=True, default='dautu')
    amount_total = fields.Float()
    progress_contract = fields.Char('Tiến độ hợp đồng')
    remaining_date = fields.Char('Ngày còn lại')
    delivery_date = fields.Datetime('Ngày giao hàng')
    state = fields.Selection([
        ('draft', 'NHÁP'),
        ('pending', 'CHỜ DUYỆT'),
        ('confirmed', 'ĐÃ CHỐT'),
        ('processing', 'ĐANG THỰC HIỆN'),
        ('completed', 'ĐÃ QUYẾT TOÁN')
    ], string='Status', readonly=True, default='draft')
    payments_contract_id = fields.One2many('contract.payments', 'contract_payment_customer', string='Payments Contract')

    ####
    def confirm_contract(self):
        self.state = 'pending'

    ####
    @api.onchange('payments_contract_id')
    def check_onchange_payments_contract_id(self):
        if self.payments_contract_id:
            total_percent = 0
            list_percent = self.payments_contract_id.mapped('percent_payment')
            for percent in list_percent:
                if percent:
                    total_percent += percent
            if total_percent > 100:
                raise ValidationError('Total Percent Payment Value must be equal to 100')
