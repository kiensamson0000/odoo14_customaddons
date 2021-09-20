from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class CreateContractWizard(models.TransientModel):
    _name = "create.contract.wizard"

    contract_id = fields.Char('Mã hợp đồng')
    contract_type = fields.Selection([
        ('hopdonghthietke', 'Hợp đồng thiết kế'),
        ('hopdongmuaban', 'Hợp đồng mua bán'),
    ], string='Loại hợp đồng', readonly=True, default='hopdonghthietke')
    contract_number = fields.Selection([
        ('stk0123/hdnvs', 'STK0123HĐNVS'),
        ('mb98123/hdmb522', 'MB98123/HĐMB522'),
    ], string='Hợp đồng khung', readonly=True, default='stk0123/hdnvs')
    infor_contract = fields.Char('Thông tin hợp đồng')
    contract_sign_date = fields.Datetime('Ngày ký hợp đồng')
    cccd_id = fields.Char('Số CCCD')
    date_created = fields.Char('Ngày cấp')
    place = fields.Char('Nơi cấp')
    signer = fields.Char('Người ký')
    signer_position = fields.Selection([
        ('giamdoc', 'Giám đốc'),
        ('truongphong', 'Trưởng phòng'),
        ('ketoan', 'Kế toán'),
    ], string='Chức vụ', readonly=True, default='giamdoc')
    contract_address = fields.Char('Địa chỉ hợp đồng')
    contract_construction_date = fields.Datetime('Ngày thi công hợp đồng')
    delivery_address = fields.Char('Địa chỉ giao hàng')
    contract_end_date = fields.Datetime('Ngày kết thúc hợp đồng')
    category_contract = fields.Selection([
        ('dautu', 'Đầu tư'),
        ('suachua', 'Sửa chữa'),
    ], string='Hạng mục hợp đồng', readonly=True, default='dautu')
    progress_contract = fields.Char('Tiến độ hợp đồng')
    remaining_date = fields.Char('Ngày còn lại')
    delivery_date = fields.Datetime('Ngày giao hàng')
    check_contract = fields.Boolean(default=True)
    relate_sale_order = fields.Many2many('sale.order')

    def create_contract(self):
        quotation_id = self.env.context.get('active_ids', [])
        # print(self.partner_lines)
        quotation = self.env['sale.order'].browse(quotation_id[0])

        vals = {
            'contract_id': self.contract_id,
            'contract_type': self.contract_type,
            'contract_number': self.contract_number,
            'infor_contract': self.infor_contract,
            'contract_sign_date': self.contract_sign_date,
            'customer_id': quotation.partner_id.id,
            'cccd_id': self.cccd_id,
            'date_created': self.date_created,
            'place': self.place,
            'signer': self.signer,
            'order_source': quotation_id[0],
            'signer_position': self.signer_position,
            'contract_address': self.contract_address,
            'contract_construction_date': self.contract_construction_date,
            'delivery_address': self.delivery_address,
            'contract_end_date': self.contract_end_date,
            'category_contract': self.category_contract,
            'progress_contract': self.progress_contract,
            'remaining_date': self.remaining_date,
            'delivery_date': self.delivery_date,
            'state': 'draft',
        }
        self.env['contract.management'].create(vals)
        contract_id = self.env['contract.management'].search([('order_source', '=', quotation_id[0])], limit=1).id
        quotation.write({'contract':contract_id})
