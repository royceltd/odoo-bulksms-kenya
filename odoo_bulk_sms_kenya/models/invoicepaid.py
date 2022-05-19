# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_validate_invoice_payment(self):
        """ Posts a payment used to pay an invoice. This function only posts the
        payment by default but can be overridden to apply specific post or pre-processing.
        It is called by the "validate" button of the popup window
        triggered on invoice form by the "Register Payment" button.
        """

        if any(len(record.invoice_ids) != 1 for record in self):
            # For multiple invoices, there is account.register.payments wizard
            raise UserError(_("This method should only be called to process a single invoice's payment."))

        # Sends Text Message to Partner once the invoice is paid partially or fully

        invoice_ref = self.communication
        amount = str(self.amount)
        currency = self.currency_id.display_name
        contact = self.partner_id.contact_address
        phone = self.partner_id.phone

        text_body = "Thanks " + contact + ", Your Invoice: " + invoice_ref + " has been paid for amount: " + currency + amount

        self.env['send.text'].sendCustomText(phone, text_body, 'RoyceLtd')

        return self.post()
