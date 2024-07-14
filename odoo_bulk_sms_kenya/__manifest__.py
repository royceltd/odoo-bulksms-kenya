{
    'name':'Odoo Bulk SMS Kenya',
    'summary':'Integrate bulk sms into odoo ERP in kenya',
    'version':'16.0.1.0.0',
    'category':'Tools',
    'author':'Royce Technologies',
    'maintainer':'Royce Technologies',
    'company':'Royce Technologies',
    'website':'https://roycebulksms.com',
    'depends':['base'],
    'data':[
        'views/sendtext.xml',
        'views/senttext.xml',
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/menu.xml',
        'views/contacts.xml',
        'views/sendgrouptext.xml',
    ],
    'images': ['static/description/sms-services-sms.png'],
    'license':'AGPL-3',
    'application':False,
    'installable':True,
    'auto_install':False


}