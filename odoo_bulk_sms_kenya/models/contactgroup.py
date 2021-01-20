# -*- coding: utf-8 -*-
from odoo import models, fields

class ContactGroup(models.Model):
    _name='royce.contactgroups'
    name=fields.Char(required=True)
    description=fields.Text(required=False)