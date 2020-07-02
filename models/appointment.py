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

    def delete_lines(self):
        for rec in self:
            print('rec', rec)
            rec.appointment_lines = [(5,0,0)]

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result= super(HospitalAppointment, self).create(vals)
        return result
    # overite write function odoo
    @api.multi
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print("Test Write Function")
        return res


    name= fields.Char('Appointment ID', required=True, copy=False, readOnly=True, index=True, default=lambda self: _('New'))
    patient_id= fields.Many2one('hospital.patient', string='Patient ID', required=True)
    doctor_id=fields.Many2one('hospital.doctor', string='Doctor')
    #doctor_ids=fields.Many2many('hospital.doctor', 'hospital_patient_rel', 'appointment_id', 'doctor_id_rec',string='Doctor')
    patient_name= fields.Char('Patient Name',related='patient_id.patient_name')
    patient_age= fields.Integer('Age' , related='patient_id.patient_age')
    notes= fields.Text('Registration Note')
    appointment_date= fields.Date('Date', required=True)
    doctor_note = fields.Text('Note')
    appointment_lines= fields.One2many('hospital.appointment.lines','appointment_id',string='Appointment Lines')
    pharmacy_note = fields.Text('Note')
    state = fields.Selection([
            ('draft','Draft'),
            ('confirm', 'Confirm'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],string='Status', readonly=True, default='draft')

class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointent lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty= fields.Integer('Quantity')
    appointment_id= fields.Many2one('hospital.appointment', string='Appointment ID')