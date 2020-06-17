from odoo import models, fields

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Record'

    name= fields.Char()
    gender = fields.Selection([
        ('male','Male'),
        ('female', 'Female'),
    ], default='male', string="Gender")
    user_id=fields.Many2one('res.users', string='Related User')
    #appointment_ids = fields.Many2many('hospital.appointment', 'hospital_patient_rel', 'doctor_id_rec', 'appointment_id', string='Appointment')