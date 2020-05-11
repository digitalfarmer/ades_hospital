from odoo import  models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'patient record'
    _rec_name = 'name_seq'

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('The age Must be greater then 5'))

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age<25:
                    rec.age_group = 'minor'
                else:
                    rec.age_group= 'mayor'

    @api.multi
    def open_patient_appointments(self):
        return {
            'name':_('Appointments'),
            'domain':[('patient_id','=', self.id)],
            'view_type': 'form',
            'res_model':'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id','=', self.id)])
        self.appointment_count = count

    def _get_default_note(self):
        return "Pastikan Data di Isi dengan lengkap"

    patient_name= fields.Char('Pstient Name', reuired=True)
    patient_age= fields.Integer('Age', track_visibility='always')
    notes= fields.Text('Registration Notes', default=_get_default_note)
    image= fields.Binary('Image', attachment=True)
    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Patient ID', reuired=True, copy=False, readonly=True,
                           index=True, default=lambda self: _("New"))
    appointment_count = fields.Integer('Appointment', copute='get_appointment_count')
    active= fields.Boolean("Active", default=True)

    gender = fields.Selection([
        ('male','Male'),
        ('female', 'Female'),
        ('transg', 'Trans Gender'),
    ],default='male',string='Gender')
    age_group= fields.Selection([
        ('mayor','Mayor'),
        ('minor', 'Minor')
    ], string='Age Group', compute='set_age_group')
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result