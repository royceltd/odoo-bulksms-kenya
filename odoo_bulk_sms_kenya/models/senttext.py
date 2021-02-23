# -*- coding: utf-8 -*-
from odoo import models, fields

class SentText(models.Model):
    _name='sent.text'
    _order = "id desc"
    text_message=fields.Text(string="Messaqge", required=True)
    sender_id=fields.Char(string="Sender Id", required=True)
    phone_number=fields.Char(required=True)
    status=fields.Char(required=True)
    message_id=fields.Char()
    response_code=fields.Char()
    response_description=fields.Char()
    network_id=fields.Char()
    delivery_status=fields.Char()
    delivery_description=fields.Char()
    delivery_tat=fields.Char()
    delivery_networkid=fields.Char()
    delivery_time=fields.Char()
    delivery_code=fields.Char()
    delivery_network_id=fields.Char()
    delivery_response_description=fields.Char()
