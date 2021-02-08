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
        mobiles = self.phone_number.split(", ")
        for mobile in mobiles:
            self.sendmessage(mobile);
    @api.multi
    def button_reset(self):
       for rec in self:
           rec.write({'status': 'draft'})

    @api.multi
    def button_cancel(self):
       for rec in self:
           rec.write({'status': 'cancelled'})

    def sendmessage(self,mobile):

        # step 1 get api key
        latest_apikey = self.env['api.keys'].search([], limit=1, order='create_date desc')
        apikey = latest_apikey.apikey

        endpoint = "https://bulksms.roycetechnologies.co.ke/api/sendmessage"
        data = {

            'sender_id': self.sender_id, 'text_message': self.text_message, 'phone_number': mobile
        }

        headers = {

            "Authorization": "Bearer " + apikey
        }

        response = requests.post(endpoint, data=data, headers=headers).json()

        self.env['sent.text'].create(

            {'text_message': self.text_message, 'sender_id': self.sender_id.name,
             'phone_number':mobile,'status':'Sent'})


        for rec in self:
            rec.write({'status': 'sent'})
        # print (response)
