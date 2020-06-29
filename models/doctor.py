from odoo import models, fields, api
import requests
# import telebot
# bot = telebot.TeleBot("460069520:AAF0WiA42CqwSAZqJmBUxTiTFaUGGKxIreY")

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

    # @bot.message_handler(commands=['start', 'help'])
    # def send_notif_telegram(message):
    #    bot.reply_to(message, "Howdy, how are you doing?")
    @api.multi
    def send_notif_telegram(self):
        pass