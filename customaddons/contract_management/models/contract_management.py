from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError

class ContractManagement(models.Model):
    _name = "contract.management"
    _description = "Contract Management"
    _rec_name = 'order_source'

    contract_id = fields.Char('Mã hợp đồng')
    contract_type = fields.Selection([
        ('hopdonghthietke', 'Hợp đồng thiết kế'),
        ('hopdongmuaban','Hợp đồng mua bán')
    ], string='Loại hợp đồng', default='hopdonghthietke')
    contract_number = fields.Selection([
        ('stk0123/hdnvs','STK0123HĐNVS'),
        ('mb98123/hdmb522','MB98123/HĐMB522'),
    ], string='Hợp đồng khung', default='stk0123/hdnvs')
    infor_contract = fields.Char('Thông tin hợp đồng')
    contract_sign_date = fields.Datetime('Ngày ký hợp đồng')
    # XU LY LAY TEN THEO DON HANG
    # name_customer = fields.Char('Tên Khách')
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
    progress_contract = fields.Char('Tiến độ hợp đồng')
    remaining_date = fields.Char('Ngày còn lại')
    delivery_date = fields.Datetime('Ngày giao hàng')
    sent = fields.Boolean(string='Sent or not', default=False)
    edited = fields.Boolean(string='Edited or not', default=False)
    state = fields.Selection([
        ('draft','NHÁP'),
        ('pending','CHỜ DUYỆT'),
        ('confirmed','ĐÃ CHỐT'),
        ('processing','ĐANG THỰC HIỆN'),
        ('completed','ĐÃ QUYẾT TOÁN'),
    ], string='Status', readonly=True, default='draft', tracking=True)

    def confirm_contract(self):
        self.sent = True
        self.state = 'pending'

    ##### test
    @api.onchange('contract_id', 'contract_type', 'contract_number')
    def _change_state_when_edited(self):
        self.state = 'draft'
        self.sent = False
        self.edited = True

