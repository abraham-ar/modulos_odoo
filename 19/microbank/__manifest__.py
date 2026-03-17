{
    'name' : 'MicroBank',
    'depends' : [
        'base',
    ],
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/client_views.xml', 'views/loan_application_views.xml', 'views/loan_payment_views.xml',
        'views/menus.xml',
    ]
}