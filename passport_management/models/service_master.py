from odoo import models,fields,api

class ServiceMaster(models.Model):
    _name = 'service.master'
    _description = 'Service Master'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Service Name")
    description = fields.Text(string="Description")
    type_ids = fields.Many2many('service.type', string="Service Type" )
    website_image = fields.Image(string="Website Icon")


class ServiceType(models.Model):
    _name = 'service.type'
    _description = 'Service Type '
    _inherit = ['mail.thread', 'mail.activity.mixin']    
    
    name = fields.Char(string="Service Type")
    fees_amount = fields.Float(string="Service Charge", tracking=True)
    description = fields.Text(string="Description")
    parent_id = fields.Many2one('service.master', string="Service Master")
    document_ids = fields.Many2many('service.document',string="Documents")
    document_type_ids = fields.Many2many('document.type', string="Document Type", tracking=True)



    @api.onchange('document_type_ids')
    def onchange_document_type(self):
        vals_list = []
        self.document_ids = False
        for rec in self.document_type_ids:
            self.document_ids = [(4, doc.id)for doc in rec.document_ids]
            
            
    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None):
        domain = []
        if 'service_id' in self._context:
            service_id = self._context.get('service_id')
            if service_id:
                service_id = self.env['service.master'].search([('id', '=', service_id)])
                service_type_ids = service_id.type_ids.ids
                domain += [('id', 'in', service_type_ids)]
        res = super(ServiceType, self)._name_search(name=name, domain=domain, operator=operator, order=order, limit=limit)
        return res