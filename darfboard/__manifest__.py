{
    'name': "Darfboard ICO control",
    'version': '1.0',
    'depends': ['base',
                'sale',
                'sales_team',
                'delivery',
                'barcodes',
                'mail',
                'report',
                'portal_sale',
                'website_portal',
                'website_payment',],
    'author': "Darfchain",
    'category': 'Application',
    'description': """
    Module for synchronization with ICO ERP with IPFS
    """,
    'data': [
     'views/setting_journals.xml',
     #'views/journal_signature.xml',
     
    ],
}