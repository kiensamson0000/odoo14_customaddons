from odoo import fields, models, api


class CreatePlanSaleWizard(models.TransientModel):
    _name = 'create.plan.sale.wizard'

    name_plan_sales = fields.Char(string="Name Plan Sales", require=True)
    information_plan_sales = fields.Text(string="Information Plan Sale", require=True)


    # sale_order_ids_wizard = fields.Many2many("sale.order")
    id_quotation = fields.Many2one("sale.order")

    # res_partner_ids = fields.Many2many("res.partner", string="Approval")
    form_approval_wizard = fields.Many2many("plan.sale.order", string="Inspector")


    def action_create_plan_sale(self):
        for rec in self:
            # rec.id_quotation.message_post(body="Request create plan sale",
            #                               message_type='notification',
            #                               subtype_xmlid='mail.mt_comment',
            #                               partner_ids=rec.form_approval_wizard.res_partner_form_approval.ids)

            rec.id_quotation.sender_name = rec.name_plan_sales
            rec.id_quotation.information_plan = rec.information_plan_sales
            # result = []
            # for rec in self:
            #     rec_name = rec.name_plan_sales, rec.information_plan_sales, rec.id_quotation
            #     result.append((rec.id, rec_name))
            # return result