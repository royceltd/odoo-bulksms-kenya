{
    'name': 'Bulk SMS for Customers & Suppliers',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Send bulk SMS to customers and suppliers via existing SMS infrastructure',
    'description': '''
        Bulk SMS for Customers & Suppliers
        ==================================
        
        Features:
        * Send SMS to all customers or selected customers
        * Send SMS to all suppliers or selected suppliers
        * Filter by customer/supplier categories
        * Reuse existing SMS templates and configuration
        * Integration with existing Bulk SMS Kenya module
        * Customer/Supplier specific SMS logging
        
        Dependencies: Requires odoo_bulk_sms_kenya module
    ''',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'contacts', 'sale', 'purchase', 'odoo_bulk_sms_kenya'],
    'data': [
        'security/customer_sms_security.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/customer_sms_log_views.xml',
        'wizard/customer_sms_wizard_views.xml',
        'wizard/supplier_sms_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
