from odoo import models, fields, api
from odoo.exceptions import UserError
import re


class SmsBulkPasteWizard(models.TransientModel):
    _name = 'royce.sms.bulk.paste.wizard'
    _description = 'Send SMS to Custom Phone Numbers'

    template_id = fields.Many2one('royce.sms.royce.template', 'SMS Template')
    custom_message = fields.Text('Custom Message')
    phone_numbers_text = fields.Text('Phone Numbers', required=True)
    message_preview = fields.Text('Message Preview', readonly=True)
    
    # Statistics
    total_numbers = fields.Integer('Total Numbers', default=0)
    valid_numbers = fields.Integer('Valid Numbers', default=0)
    invalid_count = fields.Integer('Invalid Numbers', default=0)

    @api.onchange('phone_numbers_text')
    def _onchange_phone_numbers(self):
        """Update statistics when phone numbers change"""
        if self.phone_numbers_text:
            lines = [l.strip() for l in self.phone_numbers_text.split('\n') if l.strip()]
            self.total_numbers = len(lines)
            
            valid = sum(1 for line in lines if self._validate_phone(line))
            self.valid_numbers = valid
            self.invalid_count = self.total_numbers - valid

    @api.onchange('template_id', 'custom_message')
    def _onchange_message(self):
        """Update message preview"""
        if self.template_id:
            sample_record = type('obj', (object,), {'name': 'John Doe'})
            self.message_preview = self.template_id.render_template(self.template_id.body, sample_record)
        else:
            self.message_preview = self.custom_message or ''

    def _clean_phone_number(self, phone):
        """Clean and validate phone number"""
        if not phone:
            return None
        
        clean = re.sub(r'\D', '', str(phone))
        
        if clean.startswith('0'):
            clean = '254' + clean[1:]
        elif clean.startswith('254'):
            pass
        elif clean.startswith('7') and len(clean) == 9:
            clean = '254' + clean
        
        if len(clean) == 12 and clean.startswith('254'):
            return f"+{clean}"
        
        return None

    def _validate_phone(self, phone):
        """Check if phone number is valid"""
        return self._clean_phone_number(phone) is not None

    def _parse_phone_numbers(self, text, validate=True):
        """Parse phone numbers from text"""
        if not text:
            return []
        
        lines = text.strip().split('\n')
        phone_list = []
        
        for line in lines:
            phone = line.strip()
            if not phone:
                continue
            
            cleaned = self._clean_phone_number(phone)
            if cleaned:
                phone_list.append(cleaned)
            elif not validate:
                phone_list.append(phone)
        
        return phone_list

    def send_sms(self):
        """Send SMS to all pasted phone numbers"""
        
        if not self.template_id and not self.custom_message:
            raise UserError('Please select a template or enter a custom message.')
        
        phone_numbers = self._parse_phone_numbers(self.phone_numbers_text, validate=True)
        
        if not phone_numbers:
            raise UserError('No valid phone numbers found. Please check your input.')
        
        # Get active SMS configuration for sender_id
        try:
            config = self.env['royce.sms.config'].get_active_config()
        except Exception as e:
            raise UserError(f'SMS Configuration Error: {str(e)}')
        
        sms_log = self.env['royce.sms.log']
        
        success_count = 0
        failed_count = 0
        failed_numbers = []
        
        print(f"Starting to send {len(phone_numbers)} SMS messages using sender ID: {config.sender_id}...")
        
        for idx, phone_number in enumerate(phone_numbers, 1):
            try:
                if self.template_id:
                    sample_record = type('obj', (object,), {'name': 'Recipient'})
                    message = self.template_id.render_template(self.template_id.body, sample_record)
                else:
                    message = self.custom_message
                
                result = sms_log.send_sms(
                    phone_number=phone_number,
                    message=message,
                    recipient_name=f'Bulk Paste - {idx}',
                    template_id=self.template_id.id if self.template_id else None,
                    recipient_type='custom_bulk',
                    recipient_id=0
                )
                
                if result['success']:
                    success_count += 1
                    print(f"✓ SMS sent to {phone_number}")
                else:
                    failed_count += 1
                    failed_numbers.append(phone_number)
                    print(f"✗ Failed to send to {phone_number}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                failed_count += 1
                failed_numbers.append(phone_number)
                print(f"✗ Exception sending to {phone_number}: {str(e)}")
        
        message = f"SMS Sending Completed!\n\nSuccess: {success_count}\nFailed: {failed_count}"
        
        if failed_numbers and len(failed_numbers) <= 5:
            message += f"\n\nFailed numbers:\n" + "\n".join(failed_numbers)
        elif failed_numbers:
            message += f"\n\n{len(failed_numbers)} numbers failed (see SMS Log for details)"
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'SMS Sent',
                'message': message,
                'type': 'success' if failed_count == 0 else 'warning',
                'sticky': False,
            }
        }