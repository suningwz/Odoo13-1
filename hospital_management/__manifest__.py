# -*- coding: utf-8 -*-
{
    'name': "hospital_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'hr', 'account', 'sale','odoo_report_xlsx'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hospital_management.xml',
        'views/appointment.xml',
        'views/appointment_smartbutton.xml',
        'views/op_smartbutton.xml',
        'views/doctor_fee.xml',
        'views/op_search_view.xml',
        'views/appointment_search_view.xml',
        'data/sequence.xml',
        'data/invoice_seq.xml',
        'data/op_sequence.xml',
        'data/appointment_seq.xml',
        'data/data.xml',
        'wizard/medical_report_generation.xml',
        'reports/report.xml',
        'reports/patient_card.xml',
        # 'reports/hospital_report_views.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
