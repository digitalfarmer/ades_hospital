# -*- coding: utf
from odoo import models, fields, api, _

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread','mail.activity.mixin']

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result= super(HospitalAppointment, self).create(vals)
        return result

    name= fields.Char('Appointment ID', required=True, copy=False, readOnly=True, index=True, default=lambda self: _('New'))
    patient_id= fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age= fields.Integer('Age' , related='patient_id.patient_age')
    notes= fields.Text('Registration Note')
    appointment_date= fields.Date('Date', required=True)