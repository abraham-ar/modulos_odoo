{
    'name': 'MicroBank',
    'depends': [
        'base',
        'mail'
    ],
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml', 'data/email_templates.xml',
        'wizard/wizard.xml',
        'report/loan_agreement_template.xml',
        'views/client_views.xml', 'views/loan_application_views.xml', 'views/loan_payment_views.xml',
        'views/menus.xml',
    ]
}
