{
    'name': 'Consultancy Management',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'summary': 'Consultancy Management ERP',
    'description': """
Consultancy Management ERP for managing consultancy services,
appointments, documents, and reports in Odoo 17.
""",
    'author': 'Payal',
    'website': 'https://gitlab.com/isha6445',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'mail',
        'contacts',
        'account',
        'whatsapp_base'
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/appointment_sequence_data.xml',
        'data/service_type_data.xml',
        'data/cron.xml',
        'data/city_type_data.xml',
        'reports/report.xml',
        'reports/appointment_schedule_report.xml',
        'wizard/appointment_payment.xml',
        'views/service_document_view.xml',
        'views/passport_appointment_view.xml',
        'views/service_portal_template.xml',
        'views/dashboard_portal_template.xml',
        'views/appointment_portal_form.xml',
        'views/passport_city_view.xml',
        'views/passport_city_center_view.xml',
        'views/menu.xml',
    ],

    'assets': {
        'web.assets_frontend': [],
    },

    'images': [
        'static/description/icon.png',
        'static/description/index.html', 
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
    'price': 0.0,
    'currency': 'USD',
}
