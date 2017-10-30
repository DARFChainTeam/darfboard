{
    'name': "Darfboard ICO control reports",
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
    Module for reading information about ICO ERP with IPFS
    """,
    'data': [
     'views/setting_import.xml',
     'views/import_data.xml',
     'reports/report_entry.xml',
     
    ],
}