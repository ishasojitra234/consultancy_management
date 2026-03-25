from datetime import date, datetime
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import html2text


class Appointment(models.Model):
    _name = 'appointment.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Name", copy=False, default=lambda self: _('New'), readonly=True, tracking=True)
    customer_id = fields.Many2one('res.partner', string="Customer" , tracking=True)
    service_master_id = fields.Many2one('service.master', string= "Service" , tracking=True)
    services = fields.Char(string="Service", default='Passport')
    service_type = fields.Selection([('Fresh Passport', 'Fresh Passport'), ('Re-Issue Of Passport', 'Re-Issue Of Passport'), ('PCC', 'PCC')], string="Passport")
    service_type_id = fields. Many2one('service.type', string="Service Type" )
    state = fields.Selection([('Draft', 'Draft'), ('Confirm', 'Confirm'), 
                               ('In Process', 'In Process'), ('Get Appointment', 'Get Appointment'),
                               ('Office Visit', 'Office Visit'),('Police Verification','Police Verification'),
                               ('Done','Done'), ('Cancel', 'Cancel')], string="Status", default='Draft' , tracking=True)
    fees_amount = fields.Float(string="service Charge", tracking=True)
    first_name = fields.Char(string="First Name" , tracking=True)
    mid_name = fields.Char(string="Middle Name" , tracking=True)
    last_name = fields.Char(string="Last Name" , tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender" , tracking=True)
    nationality = fields.Many2one("res.country" , string = "Nationality")
    email = fields.Char(string="Email", tracking=True)
    phone = fields.Char(string="Phone Number", tracking=True)
    mobile = fields.Char(string="Mobile", tracking=True)
    street1 = fields.Char(string="street1")
    street2 = fields.Char(string="street2") 
    city_id = fields.Many2one("res.city", string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    pincode = fields.Char(string="ZIP")
    country_id =  fields.Many2one("res.country" , string = "Country")
    aadhar_number = fields.Char(string="Aadhar Number", tracking=True)
    pan_number = fields.Char(string="PAN Number", tracking=True)
    voter_id_number = fields.Char(string="Voter ID Number", tracking=True)
    booking_date = fields.Date(string="Date" , default=fields.Date.today())
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)
    appointment_doc_ids = fields.One2many('appointment.document' ,'appointment_id' ,string="Appointment Document", tracking=True)
    passport_id = fields.Char(string="Passport Id", tracking=True)
    password = fields.Char(string="Password", tracking=True)
    passport_type = fields.Selection([('Tatkal','Tatkal'),('Normal','Normal')], string="Passport Type", tracking=True)
    ar_number = fields.Char(string="Application Number", tracking=True)
    file_number = fields.Char(string="File Number", tracking=True)
    booklet_type = fields.Selection([('36 Page','36 Pages'),('60 Pages','60 Pages')],string="Booklets", tracking=True)
    verification_date = fields.Datetime(string="Appointment Date", tracking=True)
    father_name = fields.Char(string="Father Name", tracking=True)
    father_lname = fields.Char(string="Father Last Name", tracking=True)
    mother_name = fields.Char(string="Mother Name", tracking=True)
    mother_lname = fields.Char(string="Mother Last Name", tracking=True)
    guardian_name = fields.Char(string="Guardian Name", tracking=True)
    guardian_lname = fields.Char(string="Guardian Last Name", tracking=True)
    spouse_name = fields.Char(string="Spouse Name", tracking=True)
    spouse_lname = fields.Char(string="Spouse Last Name", tracking=True)
    payment_count = fields.Integer(string="Payment", compute = '_compute_payment_count')
    payment_ids = fields.One2many('account.payment', 'appointment_id', string= "Appointment", tracking=True)
    paid_amount = fields.Float(string='Paid Amount', tracking=True)
    due_amount = fields.Float(string='Due Amount', compute='_compute_due_amount', tracking=True)
    doucument_ids = fields.One2many('service.document', 'appointment_id', string="Documents")
    document_count = fields.Integer(string="Documents" , compute = '_compute_document_count')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    office_address_ids = fields.One2many('office.address', 'city_id', string='Office Address')
    passport_city_id = fields.Many2one('passport.city', string="Passport City")
    office_address_id = fields.Many2one('office.address', string="Passport Office Address")
    birth_space = fields.Char(string="Birth Place")
    marital_status = fields.Selection(
        [
            ('Single', 'Single'),
            ('Married', 'Married'),
            ('widow/Widower', 'Widow/Widower'),
            ('Separated', 'Separated'),
            ('Divorced', 'Divorced'),
        ],
        string="Marital Status",
    )
    re_issue_reason = fields.Selection(
        [
            ('Change In Existing Personal Particulars','Change In Existing Personal Particulars'),
            ('Damaged Passport','Damaged Passport'),
            ('Exhaustion Of Pages','Exhaustion Of Pages'),
            ('Lost Passport','Lost Passport'),
            ('Validity Expired More Than 3 Years Ago','Validity Expired More Than 3 Years Ago'),
            ('Validity Expired Within 3 Years/Due To Expire','Validity Expired Within 3 Years/Due To Expire'),
            ('Other','Other'),
            ],
            string="Reason For Re-issue",
    )
    change_in_existing_personal_particulars = fields.Many2many('change.particulars', string="Change In Existing Personal Particulars")
    father_passport_number = fields.Char(string="Father/Legal Guardian's Passport/File Number")
    father_nationality = fields.Char(string="Father/Legal Guardian's Nationality")
    mother_passport_number = fields.Char(string="Mother/Legal Guardian's Passport/File Number")
    mother_nationality = fields.Char(string="Mother/Legal Guardian's Nationality")
    old_passport_number = fields.Char(string="Old Passport Number")
    old_passport_issue_date = fields.Date(string="Old Passport Issue Date")
    old_passport_expiry_date = fields.Date(string="Old Passport Expiry Date")
    old_passport_place_of_issue = fields.Char(string="Old Passport Place Of Issue")
    new_passport_number = fields.Char(string="New Passport Number")
    new_passport_issue_date = fields.Date(string="New Passport Issue Date")
    new_passport_expiry_date = fields.Date(string="New Passport Expiry Date")
    new_passport_place_of_issue = fields.Char(string="New Passport Place Of Issue")
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)
    address = fields.Char(string="Address", compute="_compute_Address", store=True)

    @api.depends('street1', 'street2', 'city_id', 'state_id', 'pincode', 'country_id')
    def _compute_Address(self):
        for rec in self:
            city = rec.city_id.name if rec.city_id else ''
            state = rec.state_id.name if rec.state_id else ''
            country = rec.country_id.name if rec.country_id else ''
            rec.address = ' '.join(
                filter(None, [rec.street1, rec.street2, city, state, rec.pincode, country])
            )


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


    @api.onchange('passport_city_id')
    def onchange_passport_city(self):
        if self.passport_city_id:
            self.office_address_id = False


    # @api.onchange('service_type')
    # def onchange_service_type(self):
    #     if self.Re-Issue Of Passport:
    #         self.old_passport_number = ''
    #         self.old_passport_issue_date = ''
    #         self.old_passport_expiry_date = ''
    #         self.old_passport_place_of_issue = ''

    
         


    def send_whatsapp_message(self):
        for rec in self:
            message = f"Dear {rec.first_name},\n"
            message += f"This is an update regarding your passport process with *{self.company_id.name}*.\n"
            state_messages ={
                                'Confirm': (
                                    "🌟 Great news! Your application has been *confirmed*! "
                                    "We have successfully received all required documents and are preparing the next steps for you.\n"
                                ),
                                'In Process': (
                                    "🔄 Your application is *in process*! Our expert team is working on your case, and we'll keep you updated every step of the way.\n"
                                ),
                                'Get Appointment': (
                                    f"📅 Your *appointment* has been scheduled for *{self.verification_date}*. "
                                    "Please check your email for details, and make sure to carry all necessary documents. "
                                    "If you have any questions, feel free to contact us!\n"
                                ),
                                'Office Visit': (
                                    "🏢 It's time for the next step! Please visit the *passport office* as instructed for your application process. "
                                    "Carry all relevant documents and identification to ensure a smooth experience. For assistance, we're just a call away!\n"
                                ),
                                'Police Verification': (
                                    "👮 Your application is now in the *police verification* stage. "
                                    "Kindly cooperate with the local authorities to complete this process quickly and efficiently. "
                                    "For any questions, we’re here to help!\n"
                                ),
                                'Done': (
                                    "🎉 Congratulations! Your passport process is *completed*! "
                                    "You'll receive further details and your passport soon. Thank you for trusting us to assist you!\n"
                                ),
                                'Cancel': (
                                    "❌ We're sorry to inform you that your application has been *cancelled*. "
                                    "For more information or to reapply, please contact our support team at your earliest convenience. "
                                    "We're here to help!\n"
                                ),
                            }

            message += state_messages.get(self.state, f"The current status of your application is: *{self.state}*.\n")
            message += f"\nThank you for choosing *{self.company_id.name}*.\n"

            rec.company_id.send_to_whatsapp(
                whatsapp_number=rec.mobile,
                text_message=message
            )

    def send_whatsapp_draft_message(self):
        for rec in self:
            message = f"Dear {rec.first_name},\n"
            message += f"This is an update regarding your *{rec.service_type}* process with *{rec.company_id.name}*.\n\n"
            message += f"Name: {rec.first_name or ''} {rec.mid_name or ''} {rec.last_name or ''}\n"
            message += f"Gender: {rec.gender or 'N/A'}\n"
            message += f"Address: {rec.address or 'N/A'}\n"
            message += f"Marital Status: {rec.marital_status or 'N/A'}\n"
            message += f"Date of Birth: {rec.date_of_birth.strftime('%d-%m-%Y') if rec.date_of_birth else 'N/A'}\n"
            message += f"Aadhar Number: {rec.aadhar_number or 'N/A'}\n"
            message += f"Father Name: {rec.father_name or ''} {rec.father_lname or ''}\n"
            message += f"Mother Name: {rec.mother_name or ''} {rec.mother_lname or ''}\n"
            if rec.spouse_name:
                message += f"Spouse Name: {rec.spouse_name or ''} {rec.spouse_lname or ''}\n\n"
            if rec.guardian_name:
                message += f"Guardian Name: {rec.guardian_name or ''} {rec.guardian_lname or ''}\n\n"
            if rec.date_of_birth:
                today = date.today()
                age = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
                if age < 15:
                    message += "📌 *Additional Information for Minors:*\n"
                    message += f"Father/Legal Guardian's Passport/File Number: {rec.father_passport_number or 'N/A'}\n"
                    message += f"Father/Legal Guardian's Nationality: {rec.father_nationality or 'N/A'}\n"
                    message += f"Mother/Legal Guardian's Passport/File Number: {rec.mother_passport_number or 'N/A'}\n"
                    message += f"Mother/Legal Guardian's Nationality: {rec.mother_nationality or 'N/A'}\n\n"

            if rec.passport_type and rec.service_type.strip() == "Re-Issue Of Passport":
                message += "📌 *Old Passport Details (Required for Re-Issue):*\n"
                message += f"Old Passport Number: {rec.old_passport_number or 'N/A'}\n"
                message += f"Old Passport Issue Date: {rec.old_passport_issue_date.strftime('%d-%m-%Y') if rec.old_passport_issue_date else 'N/A'}\n"
                message += f"Old Passport Expiry Date: {rec.old_passport_expiry_date.strftime('%d-%m-%Y') if rec.old_passport_expiry_date else 'N/A'}\n"
                message += f"Old Passport Place Of Issue: {rec.old_passport_place_of_issue or 'N/A'}\n\n"

            message += "📋 *Please Verify Your Details:*\n"
            message += "We have received the following details for your application. Kindly review them and let us know if there are any corrections needed:\n\n"
            message += "✅ If everything is correct, no further action is needed. Please reply with '✅' to confirm.\n"
            message += "❌ If there are any errors, please reply with the correct details.\n"

            message += f"The current status of your application is: *{rec.state}*.\n"
            message += f"\nThank you for choosing *{rec.company_id.name}*.\n"

            rec.company_id.send_to_whatsapp(whatsapp_number=rec.mobile, text_message=message)



    def _send_reminder_email(self):
        appointment_ids = self.env['appointment.appointment'].search([('state', '=', 'Confirm')])
        for rec in appointment_ids:
            template = self.env.ref("passport_management.email_template_appointment_status").sudo()
                    
            email_values = {'email_from': self.env.company.email,
                            'email_to': rec.customer_id.email,
                            'reply_to': self.env.company.email,
                            'recipient_ids': [(6, 0, [])]}
            template.send_mail(rec.id, email_values=email_values, force_send=True, raise_exception=False)
            print("Reminder email sent to customer:", rec.customer_id.email)

               
    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'Confirm':
            self._send_reminder_email()


    @api.depends("appointment_doc_ids")
    def _compute_document_count(self):
         for rec in self:
            rec.document_count = len([doc for doc in rec.appointment_doc_ids if doc.doc_file])
    
    def action_view_document(self):
        if not any(doc.doc_file for doc in self.appointment_doc_ids):
            raise UserError("You must upload at least one document before viewing the documents.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Document',
            'view_mode': 'tree,form',
            'res_model': 'appointment.document',    
            'domain': [('appointment_id', '=', self.id), ('doc_file', '!=', False)],
            'target': 'current'
        }

    @api.depends('paid_amount', 'fees_amount')
    def _compute_due_amount(self):
        for record in self:
            record.due_amount = record.fees_amount - record.paid_amount

    def process_payment(self, payment_amount):
        if payment_amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")

        if payment_amount > self.due_amount:
            raise ValidationError("Payment amount cannot exceed the due amount.")

        self.paid_amount += payment_amount
        self.due_amount -= payment_amount

    @api.onchange('passport_type')
    def _onchange_passport_type(self):
        if self.passport_type == 'Tatkal':
            self.fees_amount += 2000
        if self.passport_type == 'Normal':
            self.fees_amount = 00
            
    def action_open_payment_wizard(self):
        wiz_id = self.env['appointment.payment.wizard'].create({'appointment_id': self.id, 'amount': self.due_amount})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment Payment',
            'res_model': 'appointment.payment.wizard',
            'view_mode': 'form',
            'res_id': wiz_id.id,
            'target': 'new',
        }


    def action_view_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',    
            'domain': [('appointment_id', '=', self.id)],
            'target': 'current'
        }


    @api.model  
    def create(self,vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('appointment.appointment') or _('New')
        return super(Appointment, self).create(vals)


    @api.onchange('document_type_ids')
    def onchange_document_type(self):
        vals_list = []
        self.document_ids = False
        for rec in self.document_type_ids:
            self.document_ids = [(4, doc.id)for doc in rec.document_ids]

            
    @api.onchange('service_type')
    def onchange_service_type(self):
        self.fees_amount = self.service_type_id.fees_amount
        self.due_amount = self.fees_amount
        
    def _compute_payment_count(self):
         for rec in self:
            rec.payment_count = len(self.payment_ids.ids)
        
    def action_change_state(self, new_state):
        for rec in self:
            if new_state == "Get Appointment" and not rec.verification_date:
                raise UserError("Verification Date is required to change the state to 'Get Appointment'.")
            rec.state = new_state   

    def action_in_draft(self):
        self.action_change_state("Draft")

    def action_in_confirm(self):
        self.action_change_state("Confirm")

    def action_in_Process(self):
        self.action_change_state("In Process")

    def action_in_Get_Appointment(self):
        self.action_change_state("Get Appointment")

    def action_in_Office_Visit(self):
        self.action_change_state("Office Visit")

    def action_in_Police_Verification(self):
        self.action_change_state("Police Verification")

    def action_in_Done(self):
        self.action_change_state("Done")

    def action_in_Cancel(self):
        self.action_change_state("Cancel")


            
    @api.onchange('customer_id')
    def onchange_customer_id(self):
        self.get_partner_details()
        
    def get_partner_details(self):
        self.first_name = self.customer_id.first_name
        self.last_name = self.customer_id.last_name
        self.street1= self.customer_id.street
        self.street2 = self.customer_id.street2
        self.email = self.customer_id.email
        self.city_id = self.customer_id.city_id
        self.state_id = self.customer_id.state_id
        self.country_id = self.customer_id.country_id
        self.pincode = self.customer_id.zip
        self.mobile = self.customer_id.mobile
        self.phone = self.customer_id.phone
        

    @api.onchange('service_type')
    def _onchange_service_type(self):
        if self.service_type_id:
            self.appointment_doc_ids = [(5, 0, 0)]
            doc_ids = self.service_type_id.document_ids
            document_vals = []
            for doc in doc_ids:
                vals = {
                    'appointment_id': self.id,
                    'doc_type_id': doc.doc_type_id.id,
                    'name': doc.id
                }
                document_vals.append((0, 0, vals))
            self.appointment_doc_ids = document_vals

    