# -*- coding: utf-8 -*-
import math
from datetime import time

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

import requests


class SendText(models.Model):
    _name = 'send.text'

    _order = "id desc"
    _rec_name = 'phone_number'

    sender_id = fields.Many2one('sender.id', required=True)
    phone_number = fields.Char(required=True)
    text_message = fields.Text(required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ], required=True, default='draft')
    days_difference = fields.Char(string="Ago", compute="_time_ago")
    create_date = fields.Datetime('Create Date', readonly=True)

    def _time_ago(self):
        for rec in self:
            time_difference = (fields.datetime.now() - rec.create_date)

            if time_difference.days == 0:
                time_diff = time_difference.seconds
                if time_diff > 59:
                    minutes = int(time_diff / 60)
                    rec.days_difference = str(minutes) + " minutes "
                if time_diff > 3599:
                    hours = int(time_diff / 3600)
                    rec.days_difference = str(hours) + " hours "
                if time_diff < 60:
                    rec.days_difference = str(time_diff) + " seconds "
            else:
                rec.days_difference = str((fields.datetime.now() - rec.create_date).days) + " days "

    @api.multi
    def button_sendtext(self):
        mobiles = self.phone_number.split(", ")
        for mobile in mobiles:
            self.sendmessage(mobile)

    @api.multi
    def button_reset(self):
        for rec in self:
            rec.write({'status': 'draft'})

    @api.multi
    def button_cancel(self):
        for rec in self:
            rec.write({'status': 'cancelled'})

    def sendmessage(self, mobile):

        # step 1 get api key
        latest_apikey = self.env['api.keys'].search([], limit=1, order='create_date desc')
        if latest_apikey:
            apikey = latest_apikey.apikey

            endpoint = "https://bulksms.roycetechnologies.co.ke/api/sendmessage"
            data = {

            'sender_id': self.sender_id.name, 'text_message': self.text_message, 'phone_number': mobile
        }

            headers = {

                "Authorization": "Bearer " + apikey
            }

            response = requests.post(endpoint, data=data, headers=headers).json()

            self.env['sent.text'].create(

                {'text_message': self.text_message, 'sender_id': self.sender_id.name,
                 'phone_number': mobile, 'status': 'Sent'})

            for rec in self:
                rec.write({'status': 'sent'})
            # print (response
        else:
            raise ValidationError('Please add your api key')

        for rec in self:
            rec.write({'status': 'sent'})
        # print (response)
    def sendCustomText(self, mobile, text,senderid):
         # step 1 get api key
        latest_apikey = self.env['api.keys'].search([], limit=1, order='create_date desc')
        apikey = latest_apikey.apikey

        endpoint = "https://bulksms.roycetechnologies.co.ke/api/sendmessage"
        data = {

            'sender_id': senderid, 'text_message': text, 'phone_number': mobile
        }

        headers = {

            "Authorization": "Bearer " + apikey
        }

        response = requests.post(endpoint, data=data, headers=headers).json()

        self.env['sent.text'].create(

            {'text_message': text, 'sender_id': senderid,
             'phone_number':mobile,'status':'Sent'})


