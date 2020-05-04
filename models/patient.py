from odoo import  models, fields, api, _

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'patient record'
    _rec_name = 'name_seq'

    patient_name= fields.Char('Pstient Name', reuired=True)
    patient_age= fields.Integer('Age')
    notes= fields.Text('Registration Notes')
    image= fields.Binary('Image', attachment=True)
    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Patient ID', reuired=True, copy=False, readonly=True,
                           index=True, default=lambda self: _("New"))
    gender = fields.Selection([
        ('male','Male'),
        ('female', 'Female'),
        ('transg', 'Trans Gender'),
    ],default='male',string='Gender')
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result