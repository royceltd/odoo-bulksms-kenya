# -*- coding: utf-8 -*-
from odoo import models, fields

class SendGroupText(models.Model):
    _name='royce.grouptext'
    group=fields.Many2one('royce.contactgroups',required=True)
    text_message=fields.Text(required=True)