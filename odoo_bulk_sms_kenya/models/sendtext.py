# -*- coding: utf-8 -*-
from odoo import models, fields

class SendText(models.Model):
    _name='send.text'
    sender_id=fields.Many2Many('api.keys', required=True)
    phone_number=fields.Text(required=True)
    text_message=fields.Text(required=True)
