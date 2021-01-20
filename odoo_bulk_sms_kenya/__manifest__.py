{
    'name':'Odoo Bulk SMS Kenya',
    'summary':'Integrate bulk sms into odoo ERP in kenya',
    'version':'12.0.1.0.0',
    'category':'Tools',
    'author':'Royce Technologies',
    'maintainer':'Royce Technologies',
    'company':'Royce Technologies',
    'website':'https://roycetechnologies.co.ke',
    'depends':['base'],
    'data':[
        'views/sendtext.xml',
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/menu.xml',
    ],
    'images':[],
    'license':'AGPL-3',
    'application':False,
    'installable':True,
    'auto_install':False


}