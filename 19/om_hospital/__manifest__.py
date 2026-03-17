{
    'name': 'Hospital Management System',
    'author': 'Abraham',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail', 'product'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient_views.xml', 'views/patient_tag_views.xml',
        'views/patient_readonly_views.xml',
        'views/appointment_views.xml', 'views/appointment_line_views.xml',
        'views/menu.xml',
    ]

}