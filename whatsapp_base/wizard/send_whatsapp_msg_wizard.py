from odoo import models, fields, api, _    
import html2text
from odoo.exceptions import UserError


class SendWhatsappWizard(models.TransientModel):
    _name = 'send.whatsapp.wizard'
    _description = 'Send Whatsapp Wizard'

    model_id = fields.Many2one('ir.model', string='Model')
    mail_template_id = fields.Many2one('mail.template',string='Mail Template')
    message = fields.Text(string='Message', required=True)
    res = fields.Integer(string="Record")
    mobile_number = fields.Char(string="Receipents")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
 
    @api.depends('model_id')
    def onchange_model_id(self):
        if self.model_id:
            self.mail_template_id = self.env['mail.template'].search([('model_id', '=', 'model_id')], limit=1).id

    @api.onchange('mail_template_id', 'res')
    def onchange_mail_template_id_res(self):
        if self.mail_template_id and self.res:

            vals = {
                'mail_template_id': self.mail_template_id.id,
                'resource_ref': '%s,%s' % (self.mail_template_id.model, self.res),
                }

            preview = self.env['mail.template.preview'].create(vals)
            if preview and preview.body_html:
               
                self.message = html2text.html2text(preview.body_html)
            else:
                self.message = 'No content available for preview.'


    # def send_to_whatsapp(self):
    #     if not self.mobile_number:
    #         raise UserError(_("No Mobile Number Found!"))
        
    #     self.company_id.send_to_whatsapp(
    #         whatsapp_number=self.mobile_number,
    #         text_message=self.message)
            

    def send_to_whatsapp(self):
        active_ids = self._context.get('active_ids')
        if not active_ids:
            active_ids = [self.res]  # Default to the single record if no context

        records = self.env[self.model_id.model].browse(active_ids)
        
        for rec in records:
            filename = f"{rec.name}.pdf"

            # Get the message content from the email template
            template_id = self.mail_template_id or self.env.ref('sale.email_template_edi_sale')
            vals = {
                'mail_template_id': template_id.id,
                'resource_ref': '%s,%s' % (template_id.model, rec.id),
            }
            wiz_id = self.env['mail.template.preview'].create(vals)
            text_message = html2text.html2text(wiz_id.body_html)

            # Check if partner has a mobile number
            if not rec.partner_id.mobile:
                raise UserError(_("No Mobile Number Found for Partner %s!") % rec.partner_id.name)

            # Construct the URL for the PDF report
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            record_url = f"{base_url}/web?model={self.model_id.model}&id={rec.id}&view_type=form"
            pdf_url = f"{record_url}&report_type=pdf&download=true"

            # Send message via WhatsApp
            rec.company_id.send_to_whatsapp(
                media_url=pdf_url,  # URL for the PDF report
                whatsapp_number=rec.partner_id.mobile,  # Recipient's mobile number
                text_message=text_message,  # The message content
                filename=filename  # Optional: If your method supports file attachments
            )
