from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import http, fields,_


class ConsultancyManagementPortal(CustomerPortal):
    
    
    @http.route(['/ourservices'], type='http', auth='public', website=True)
    def ourServicesView(self, **kw):
        service_ids = request.env['service.master'].search([])
        vals = {'services': service_ids, 'user': request.env.user}
        return request.render("passport_management.service_menu_portal_view", vals)
    
    @http.route(['/my/dashboard'], type='http', auth='user', website=True)
    def dashboardView(self, **kw):
        appointment_obj = request.env['appointment.appointment']
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        draft_count = appointment_obj.sudo().search_count([('state', '=', 'Draft'), ('customer_id', '=', customer_id.id)])
        print("DRAFT COUNT ::::::::: ,", draft_count, customer_id)
        confirm_count = appointment_obj.sudo().search_count([('state', '=', 'Confirm'), ('customer_id', '=', customer_id.id)])
        in_process_count = appointment_obj.sudo().search_count([('state', '=', 'In Process'), ('customer_id', '=', customer_id.id)])
        get_appoitment_count = appointment_obj.sudo().search_count([('state', '=', 'Get Appointment'), ('customer_id', '=', customer_id.id)])
        office_visit_count = appointment_obj.sudo().search_count([('state', '=', 'Office Visit'), ('customer_id', '=', customer_id.id)])
        police_verification_count = appointment_obj.sudo().search_count([('state', '=', 'Police Verification'), ('customer_id', '=', customer_id.id)])
        vals = {'draft_count': draft_count, 'confirm_count': confirm_count, 'in_process_count': in_process_count, 'get_appoitment_count': get_appoitment_count, 'office_visit_count': office_visit_count, 'police_verification_count':police_verification_count, 'user': request.env.user}
        return request.render("passport_management.dashboard_menu_portal_view", vals)
    
    @http.route(['/draft/appointment'], type='http', auth='user', website=True)
    def draftAppointmentView(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        appointment_ids = request.env['appointment.appointment'].sudo().search([('state', '=', 'Draft'), ('customer_id', '=', customer_id.id)])
        vals = {'appointment_ids': appointment_ids, 'user': request.env.user}
        return request.render("passport_management.appointment_list_view_portal", vals)
    
    @http.route(['/confirm/appointment'], type='http', auth='user', website=True)
    def confirmAppointmentView(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        appointment_ids = request.env['appointment.appointment'].sudo().search([('state', '=', 'Confirm'), ('customer_id', '=', customer_id.id)])
        vals = {'appointment_ids': appointment_ids, 'user': request.env.user}
        return request.render("passport_management.appointment_list_view_portal", vals)
    
    @http.route(['/process/appointment'], type='http', auth='user', website=True)
    def processAppointmentView(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        appointment_ids = request.env['appointment.appointment'].sudo().search([('state', '=', 'In Process'), ('customer_id', '=', customer_id.id)])
        vals = {'appointment_ids': appointment_ids, 'user': request.env.user}
        return request.render("passport_management.appointment_list_view_portal", vals)
    
    @http.route(['/get/appointment'], type='http', auth='user', website=True)
    def GetAppointmentView(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        appointment_ids = request.env['appointment.appointment'].sudo().search([('state', '=', 'Get Appointment'), ('customer_id', '=', customer_id.id)])
        vals = {'appointment_ids': appointment_ids, 'user': request.env.user}
        return request.render("passport_management.appointment_list_view_portal", vals)
   

    @http.route(['/office_visit/appointment'], type='http', auth='user', website=True)
    def OfficeVisitAppointmentView(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        appointment_ids = request.env['appointment.appointment'].sudo().search([('state', '=', 'Office Visit'), ('customer_id', '=', customer_id.id)])
        vals = {'appointment_ids': appointment_ids, 'user': request.env.user}
        return request.render("passport_management.appointment_list_view_portal", vals)
   
    @http.route(['/police_verification/appointment'], type='http', auth='user', website=True)
    def PoliceVerificationAppointmentView(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        appointment_ids = request.env['appointment.appointment'].sudo().search([('state', '=', 'Police Verification'), ('customer_id', '=', customer_id.id)])
        vals = {'appointment_ids': appointment_ids, 'user': request.env.user}
        return request.render("passport_management.appointment_list_view_portal", vals)
   

    @http.route(['/appointment/form'], type='http', auth='user', website=True)
    def AppointmentformView(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)], limit=1)
        appointment = request.env['appointment.appointment'].sudo().search([('customer_id', '=', customer_id.id)], limit=1)
        if not appointment:
            return request.render("portal.not_found_page")  
        return request.render("passport_management.portal_appointment_form", {'appointment': appointment})

    @http.route(['/new/appointment'], type='http', auth='user', website=True)
    def NewAppointmentView(self, **kw):
        service_ids = request.env['service.master'].search([])
        customer_id = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)], limit=1)
        appointment = request.env['appointment.appointment'].sudo().search([('customer_id', '=', customer_id.id)], limit=1)
        if not appointment:
            return request.render("portal.not_found_page")  
        return request.render("passport_management.portal_new_appointment_form", {'appointment': appointment,'services': service_ids})

    
