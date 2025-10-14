{
    'name': 'Bulk SMS Kenya',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'summary': 'Send bulk SMS to contacts and employees via Royce Bulk SMS API',
    'description': '''
        Bulk SMS Module for Kenya
        =========================
        
        Features:
        * Configure SMS API settings (API Key, Sender ID)
        * Create and manage SMS templates with dynamic fields
        * Send SMS to contacts (all or selected)
        * Send SMS to employees (all or selected)
        * SMS delivery logging and tracking
        * User permissions (SMS Admin, SMS User)
        
        API Integration: https://roycebulksms.com/send-message
    ''',
    'author': 'Your Company',
    'website': 'https://roycebulksms.com',
    'depends': ['base', 'contacts', 'hr'],
    'data': [
        'security/sms_security.xml',
        'security/ir.model.access.csv',
        'security/ir_model.xml',           
        'wizard/sms_unified_wizard_views.xml', 
        'views/menu_views.xml',
        'views/sms_config_views.xml',
        'views/sms_template_views.xml',
        'views/sms_log_views.xml',
        'wizard/sms_contact_wizard_views.xml',
        'wizard/sms_employee_wizard_views.xml',
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}