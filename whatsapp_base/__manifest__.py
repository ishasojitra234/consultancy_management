{
    'name': 'WhatsApp Base',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Base module for WhatsApp integration',
    'description': """
Base module providing WhatsApp integration utilities
for other Odoo modules.
""",
    'author': 'Payal',
    'website': 'https://gitlab.com/isha6445',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'mail',
    ],

    'data': [
        'security/ir.model.access.csv',
        'wizard/send_whatsapp_msg_wizard_view.xml',
        'views/res_company_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
