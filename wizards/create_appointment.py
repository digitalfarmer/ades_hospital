from odoo import fields, models

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id= fields.Many2one('hospital.patient',string='Patient')
    appointment_date=fields.Date()