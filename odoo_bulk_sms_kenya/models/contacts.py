# -*- coding: utf-8 -*-
from odoo import models, fields

class Contacts(models.Model):
    _name='royce.contacts'

    first_name=fields.Char(required=True)
    other_names=fields.Char(required=False)
    phone_number=fields.Char(required=True)
    contact_group=fields.Many2one('royce.contactgroups')
    description=fields.Text(required=False)
