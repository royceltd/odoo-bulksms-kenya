# -*- coding: utf-8 -*-
from odoo import models, fields,api
import requests

class SendGroupText(models.Model):
    _name='royce.grouptext'
    _order = "id desc"
    group=fields.Many2one('royce.contactgroups',required=True)
    text_message=fields.Text(required=True)
    sender_id = fields.Many2one('sender.id', required=True)
    status=fields.Selection([
        ('draft','Draft'),
        ('sent','Sent'),
        ('cancelled','Cancelled'),
        ('failed','Failed'),
    ],required=True,default='draft')


    # @api.multi
    def button_sendtext(self):

        contacts_list = self.env['royce.contacts'].search([('contact_group','=',self.group.id)])
        for contact in contacts_list:
            # print (contact.phone_number)
            # self.env['send.text'].sendCustomText('0713727937','Text of custom module','RoyceLtd')
            self.sendmessage(contact.phone_number);

    # @api.multi
    def button_reset(self):
       for rec in self:
           rec.write({'status': 'draft'})

    # @api.multi
    def button_cancel(self):
       for rec in self:
           rec.write({'status': 'cancelled'})

    def sendmessage(self,mobile):

        # step 1 get api key
        latest_apikey = self.env['api.keys'].search([], limit=1, order='create_date desc')
        apikey = latest_apikey.apikey

        endpoint = "https://roycebulksms.com/api/sendmessage"
        data = {

            'sender_id': self.sender_id.name, 'text_message': self.text_message, 'phone_number': mobile
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