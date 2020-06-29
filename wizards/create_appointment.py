from odoo import fields, models

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id= fields.Many2one('hospital.patient',string='Patient')
    appointment_date=fields.Date('Appointment Date')


    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created From The Wizard/Code'
        }
        self.patient_id.message_post(body="Appointment Created Successfully", subject="Appointment")
        #self.env['hospital.appointment'].create(vals)

        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointment',
                'res_id': new_appointment.id,
                'context': context
                }

    def get_data(self):
        # print("Get Data Function")
        #appointment =self.env['hospital.appointment'].search([])
        appointment = self.env['hospital.appointment'].search([('patient_id','=',1)])
        print(appointment)
        for rec in appointment:
            print("Appointment Name", rec.name, "Patient ID", rec.patient_id.id)
        #print(appointment)