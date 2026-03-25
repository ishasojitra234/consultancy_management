from odoo import api,models,fields

class  ServiceDocument(models.Model):
    _name = 'service.document'
    _description = 'Service Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string="Name")
    service_type_id = fields.Many2one('service.type' , string ="Service Type")
    doc_type_id = fields.Many2one('document.type',string ="Document Type")
    appointment_id = fields.Many2one('appointment.appointment', string="Appointment")

class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'document.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string="Name")
    document_ids = fields.One2many('service.document' ,'doc_type_id', string="Document")