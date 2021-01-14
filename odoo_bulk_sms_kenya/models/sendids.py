# -*- coding: utf-8 -*-
from odoo import models, fields
class SenderId(models.Model):
    _name='sender.id'
    name=fields.Char(string='Sender Id', required=True)
