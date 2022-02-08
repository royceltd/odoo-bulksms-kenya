# -*- coding: utf-8 -*-
from odoo import models, fields


class SentText(models.Model):
    _name = 'sent.text'
    _order = "id desc"
    text_message = fields.Text(string="Messaqge", required=True)
    sender_id = fields.Char(string="Sender Id", required=True)
    phone_number = fields.Char(required=True)
    status = fields.Char(required=True)
    message_id = fields.Char()
    response_code = fields.Char()
    response_description = fields.Char()
    network_id = fields.Char()
    delivery_status = fields.Char()
    delivery_description = fields.Char()
    delivery_tat = fields.Char()
    delivery_networkid = fields.Char()
    delivery_time = fields.Char()
    delivery_code = fields.Char()
    delivery_network_id = fields.Char()
    delivery_response_description = fields.Char()
    days_difference = fields.Char(string="Ago", compute="_time_ago")
    create_date = fields.Datetime('Create Date', readonly=True),

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
