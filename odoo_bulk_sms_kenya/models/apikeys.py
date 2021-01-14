# -*- coding: utf-8 -*-
from odoo import models, fields
class ApiKeys(models.Model):
    _name='api.keys'
    name=fields.Char(required=True)
    apikey=fields.Text(required=True)