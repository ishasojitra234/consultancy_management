from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime


class AppointmentPayment(models.TransientModel): 
    _name = "appointment.payment.wizard"
    _description = "Appointment Payment wizard"
    
    appointment_id = fields.Many2one('appointment.appointment', string="Appointment")
    amount = fields.Float(string="Service Charge")
    journal_id = fields.Many2one('account.journal', string="Journal")


    def action_proceed_payment(self):
        if not self.appointment_id:
            raise ValidationError("No appointment selected.")
        self.appointment_id.process_payment(self.amount)
        
    @api.onchange('amount')
    def _onchange_amount(self):
        if self.amount and self.amount > self.appointment_id.due_amount:
            raise ValidationError("Amount can not be greter than due amount!")
           
   

    def action_create_payment(self):
        self.ensure_one()    
        if not self.appointment_id:
            raise ValidationError("No appointment selected.")
        payment = self.env['account.payment'].create(
            {'payment_type': 'inbound',
                'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                'partner_type': 'customer',
                'partner_id':self.appointment_id.customer_id.id,
                'amount': self.amount,
                'currency_id': self.env.user.company_id.currency_id.id,
                'date': datetime.today(),
                'journal_id': self.journal_id.id,
                'ref': 'Taken Payment from - ' + str(self.appointment_id.name),
                'appointment_id': self.appointment_id.id,
                'user_id': self.env.user.id})
        if payment:
            payment.action_post()
            vals = {'paid_amount': (self.appointment_id.paid_amount + self.amount)}
            print("VALS ::::::::::: ", vals)
            self.appointment_id.write(vals)