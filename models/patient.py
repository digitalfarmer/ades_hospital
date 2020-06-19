from odoo import  models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'patient record'
    _rec_name = 'name_seq'

    @api.multi
    def name_get(self):
        res =[]
        for rec in self:
            res.append((rec.id, '%s - %s' %(rec.name_seq, rec.patient_name)))
        return res

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

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    def action_send_card(self):
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def _get_default_note(self):
        return "Pastikan Data di Isi dengan lengkap"

    patient_name= fields.Char('Pstient Name', reuired=True)
    patient_age= fields.Integer('Age', track_visibility='always')
    notes= fields.Text('Registration Notes', default=_get_default_note)
    image= fields.Binary('Image', attachment=True)
    contact_number = fields.Char(string='Contact Number')
    name_seq = fields.Char(string='Patient ID', reuired=True, copy=False, readonly=True,
                           index=True, default=lambda self: _("New"))
    appointment_count = fields.Integer('Appointment', copute='get_appointment_count')
    active= fields.Boolean("Active", default=True)
    doctor_id=fields.Many2one('hospital.doctor', string='Doctor')
    email_id= fields.Char('Email')
    user_id= fields.Many2one('res.users', string='PRO')
    doctor_gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('trans','Trans Gender'),
    ], string='Doctor Gender', default='male')
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


