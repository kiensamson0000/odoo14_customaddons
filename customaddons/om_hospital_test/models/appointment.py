# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
import os


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"

    #inherit để add chatter (Send Message, Log Note, Schedule Activity Buttons), với Schedule Activity: mail.activity.mixin.   NOTE: Mỗi khi inherit thì nhớ khai báo depends trong __manifest__.py

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))  # field hien thi Sequence
    pateint_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('note'):     # nếu field 'note' bỏ trống --> values = 'New Patient'
            vals['note'] = 'New Patient'
        if vals.get('name', _('New')) == _('New'):      # create sequence for hospital_patient
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        # print("Res ---------", res) # => result = hospital.patient(7,)
        # print("Vals -------",vals)  # => result = {'state': 'draft', 'name': 'Mr. Long', 'age': 25, 'responsible_id': 35, 'gender': 'male', 'note': "I'm Long", 'message_follower_ids': [], 'activity_ids': [], 'message_ids': []}
        return res


    # function change state
    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'




