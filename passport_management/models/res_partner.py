from datetime import date
from odoo import api,models,fields
import urllib.request
from urllib.parse import quote
import requests
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(string="First Name", tracking=True)
    last_name = fields.Char(string="Last Name", tracking=True)
    journal_id = fields.Many2one('account.journal', string="Journal")
    appointment_ids = fields.One2many('appointment.appointment', 'customer_id', string= "Appointment")
    date_of_birth = fields.Date(string="Date of Birth", store=True, tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    aadhar_number = fields.Char(string="Adhar No", store=True, tracking=True)
    appointment_count = fields.Integer(string="appointment.appointment" , compute = '_compute_appointment_count')
    city_id = fields.Many2one("res.city", string="City")

    
    
    def _compute_appointment_count(self):
         for rec in self:
            rec.appointment_count = len(self.appointment_ids.ids)
               
    def action_open_customer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'tree,form',
            'res_model': 'appointment.appointment',    
            'domain': [('id', 'in', self.appointment_ids.ids)],
            'target': 'current'
        }

    @api.onchange('first_name', 'last_name')
    def _onchange_first_name_last_name(self):
        name_parts = []
        if self.first_name:
            name_parts.append(self.first_name)
        if self.last_name:
            name_parts.append(self.last_name)
        self.name = " ".join(name_parts)

    # @api.depends('date_of_birth')
    # def _compute_age(self):
    #     for rec in self:
    #         today =  date.today()
    #         if rec.date_of_birth:
    #             rec.age = today.year - rec.date_of_birth.year
    #         else:
    #            rec.age = 0
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year - (
                    (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day)
                )
            else:
                rec.age = 0          

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    appointment_id = fields.Many2one('appointment.appointment', string="Appointment")

    def archive_payment_records(self):
        """Archive selected payment records."""
        for record in self:
            record.active = False


