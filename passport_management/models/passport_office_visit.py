from odoo import api,models,fields


class PassportCity(models.Model):
    _name = 'passport.city'
    _description = 'Passport City'

    name = fields.Char(string='City Name')
    office_address_ids = fields.One2many('office.address', 'city_id', string='Office Address')
    

class PassportOfficeAddress(models.Model):
    _name = 'office.address'
    _description = 'Office Address'


    name = fields.Char(string="Office Center")
    city_id = fields.Many2one('passport.city', string="City")
    appointment_id = fields.Many2one('appointment.appointment', string="Appointment")
    street1 = fields.Char(string="street1")
    street2 = fields.Char(string="street2") 
    state_id = fields.Many2one("res.country.state", string="State")
    pincode = fields.Char(string="ZIP")
    country_id =  fields.Many2one("res.country" , string = "Country")