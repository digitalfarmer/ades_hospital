# -*- coding: utf
from odoo import models, fields, api, _

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = 'id desc'

    def action_state_confirm(self):
        for rec in self:
            rec.state= 'confirm'

    def action_state_done(self):
        for rec in self:
            rec.state= 'done'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result= super(HospitalAppointment, self).create(vals)
        return result

    name= fields.Char('Appointment ID', required=True, copy=False, readOnly=True, index=True, default=lambda self: _('New'))
    patient_id= fields.Many2one('hospital.patient', string='Patient ID', required=True)
    patient_name= fields.Char('Patient Name',related='patient_id.patient_name')
    patient_age= fields.Integer('Age' , related='patient_id.patient_age')
    notes= fields.Text('Registration Note')
    appointment_date= fields.Date('Date', required=True)
    doctor_note = fields.Text('Note')
    pharmacy_note = fields.Text('Note')
    state = fields.Selection([
            ('draft','Draft'),
            ('confirm', 'Confirm'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],string='Status', readonly=True, default='draft')