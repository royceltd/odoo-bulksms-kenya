# -*- coding: utf-8 -*-
from odoo import models, fields,api
import requests
class SendText(models.Model):
    _name='send.text'
    sender_id=fields.Many2one('sender.id', required=True)
    phone_number=fields.Text(required=True)
    text_message=fields.Text(required=True)
    status=fields.Selection([
        ('draft','Draft'),
        ('sent','Sent'),
        ('cancelled','Cancelled'),
        ('failed','Failed'),
    ],required=True,default='draft')


    @api.multi
    def button_sendtext(self):

        endpoint = "https://bulksms.roycetechnologies.co.ke/api/sendmessage"
        data ={

            'sender_id': 'RoyceLtd', 'text_message': 'Hello from python', 'phone_number': '0713727937'
        }

        headers ={

            "Authorization": "Bearer 13|iIfwqjuorHLfKuJjGHCp11MCwvjfQKbWwu1kaqVA"
        }

        response = requests.post(endpoint, data=data, headers=headers)

        print(response.json())


    @api.multi
    def button_reset(self):
       for rec in self:
           rec.write({'status': 'draft'})

    @api.multi
    def button_cancel(self):
       for rec in self:
           rec.write({'status': 'cancelled'})