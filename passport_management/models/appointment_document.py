from odoo import api, models, fields

class AppointmentDocument(models.Model):
    _name = 'appointment.document'
    _description = 'Appointment Document'
    
    name = fields.Many2one('service.document', string="Documents")
    is_require = fields.Boolean(string="Is Require?")
    doc_name = fields.Char(string="File Name")
    doc_file = fields.Binary(string="Upload File")
    doc_type_id = fields.Many2one('document.type', string="Document Type")
    appointment_id = fields.Many2one('appointment.appointment', string="Appointment")


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    appointment_id = fields.Many2one('appointment.appointment', string="Appointment")


class changeIinExistingPersonalParticulars(models.Model):
    _name = 'change.particulars'
    _description = 'Change IN Existing Personal Particulars'

    name = fields.Char(string="Name")
