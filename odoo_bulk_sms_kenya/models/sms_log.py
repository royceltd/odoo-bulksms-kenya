from odoo import models, fields, api
import requests
import json
from datetime import datetime
import re


class SmsLog(models.Model):
    _name = 'royce.sms.log'
    _description = 'SMS Log'
    _order = 'create_date desc'

    name = fields.Char('Reference', required=True)
    recipient_name = fields.Char('Recipient Name')
    phone_number = fields.Char('Phone Number', required=True)
    message = fields.Text('Message', required=True)
    sender_id = fields.Char('Sender ID')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ], 'Status', default='draft')
    error_message = fields.Text('Error Message')
    sent_date = fields.Datetime('Sent Date')
    message_id = fields.Char('Message ID', help='ID returned from RoyceTalk API')
    api_response = fields.Text('API Response', help='Full API response for debugging')
    template_id = fields.Many2one('royce.sms.royce.template', 'Template Used')
    recipient_type = fields.Selection([
        ('contact', 'Contact'),
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('notification', 'Notification'),
        ('custom', 'Custom'),
    ], 'Recipient Type', default='custom', required=True)
    recipient_id = fields.Integer('Recipient ID', required=False, help="ID of the recipient in the corresponding model (e.g., res.partner for contacts/customers/suppliers)")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    @api.model
    def send_sms(self, phone_number, message, recipient_name=None, template_id=None, recipient_type='custom', recipient_id=None):
        """Send SMS via RoyceTalk API and log the attempt"""
        
        try:
            # Get active SMS configuration
            config = self.env['royce.sms.config'].get_active_config()
            print(f"✓ Using SMS Config: {config.name} (ID: {config.id})")
            print(f"✓ API URL: {config.api_url}")
            print(f"✓ Sender ID: {config.sender_id}")
            
        except Exception as e:
            error_msg = f"Error fetching SMS config: {str(e)}"
            print(f"✗ {error_msg}")
            return {'success': False, 'error': error_msg}

        # Clean phone number
        clean_phone = self._clean_phone_number(phone_number)
        if not clean_phone:
            error_msg = f"Invalid phone number format: {phone_number}"
            print(f"✗ {error_msg}")
            return {'success': False, 'error': error_msg}
        
        print(f"✓ Cleaned phone number: {clean_phone}")

        # Create log record FIRST
        log_vals = {
            'name': f"SMS-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'recipient_name': recipient_name or 'Unknown',
            'phone_number': clean_phone,
            'message': message,  # Store the FULL message
            'sender_id': config.sender_id,
            'template_id': template_id,
            'recipient_type': recipient_type,
            'recipient_id': recipient_id,
            'status': 'draft',
        }
        log_record = self.create(log_vals)
        print(f"✓ Created log record: {log_record.name}")

        print(f"Sending SMS to {clean_phone}")
        print(f"Message: {message}")

        # Prepare API request - EXACTLY as per working script
        headers = {
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'phone_number': clean_phone,
            'sender_id': config.sender_id,
            'text_message': message
        }

        print(f"✓ Headers: {{'Authorization': 'Bearer ***', 'Content-Type': 'application/json'}}")
        print(f"✓ Payload: {json.dumps(payload, indent=2)}")

        try:
            # Send SMS via API with timeout
            response = requests.post(
                config.api_url, 
                headers=headers, 
                json=payload, 
                timeout=30
            )
            
            print(f"✓ API Response Status: {response.status_code}")
            print(f"✓ API Response Body: {response.text}")
            
            # Update log with API response
            log_record.write({
                'api_response': response.text,
            })
            
            # Handle success response
            if response.status_code == 200:
                try:
                    result = response.json()
                    
                    # Extract message ID and status from response
                    message_id = result.get('data', {}).get('message_id', '')
                    api_status = result.get('data', {}).get('status', 'sent')
                    cost = result.get('data', {}).get('cost', 0)
                    
                    print(f"✓ SMS sent successfully!")
                    print(f"  Message ID: {message_id}")
                    print(f"  Status: {api_status}")
                    print(f"  Cost: {cost}")
                    
                    # Update log record with success details
                    log_record.write({
                        'status': 'sent',
                        'sent_date': fields.Datetime.now(),
                        'message_id': message_id,
                    })
                    
                    return {
                        'success': True, 
                        'log_id': log_record.id,
                        'message_id': message_id,
                        'status': api_status
                    }
                    
                except ValueError as e:
                    error_msg = f"Failed to parse API response: {str(e)}"
                    print(f"✗ {error_msg}")
                    log_record.write({
                        'status': 'failed',
                        'error_message': error_msg
                    })
                    return {'success': False, 'error': error_msg, 'log_id': log_record.id}
                    
            else:
                # Handle error response
                error_msg = f"API Error {response.status_code}: {response.text}"
                print(f"✗ Failed to send SMS: {error_msg}")
                
                log_record.write({
                    'status': 'failed',
                    'error_message': error_msg
                })
                
                return {'success': False, 'error': error_msg, 'log_id': log_record.id}
                
        except requests.exceptions.Timeout:
            error_msg = "Request timeout - API took too long to respond"
            print(f"✗ {error_msg}")
            log_record.write({
                'status': 'failed',
                'error_message': error_msg
            })
            return {'success': False, 'error': error_msg, 'log_id': log_record.id}
            
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error - Failed to reach API server"
            print(f"✗ {error_msg}")
            log_record.write({
                'status': 'failed',
                'error_message': error_msg
            })
            return {'success': False, 'error': error_msg, 'log_id': log_record.id}
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request Error: {str(e)}"
            print(f"✗ {error_msg}")
            log_record.write({
                'status': 'failed',
                'error_message': error_msg
            })
            return {'success': False, 'error': error_msg, 'log_id': log_record.id}
            
        except Exception as e:
            error_msg = f"Unexpected Error: {str(e)}"
            print(f"✗ {error_msg}")
            log_record.write({
                'status': 'failed',
                'error_message': error_msg
            })
            return {'success': False, 'error': error_msg, 'log_id': log_record.id}

    @api.model
    def _clean_phone_number(self, phone):
        """Clean and validate phone number"""
        if not phone:
            return None
            
        # Remove all non-digit characters
        clean = re.sub(r'\D', '', str(phone))
        
        # Handle Kenyan numbers
        if clean.startswith('0'):
            clean = '254' + clean[1:]  # Replace leading 0 with 254
        elif clean.startswith('254'):
            pass  # Already in correct format
        elif clean.startswith('7') and len(clean) == 9:
            clean = '254' + clean  # Add country code
        
        # Validate length (should be 12 digits for Kenya: 254XXXXXXXXX)
        if len(clean) == 12 and clean.startswith('254'):
            return f"+{clean}"  # Return with + prefix for API
        
        return None

    def retry_send(self):
        """Retry sending failed SMS"""
        self.ensure_one()
        if self.status != 'failed':
            return {'warning': {'title': 'Warning', 'message': 'Can only retry failed messages'}}
        
        result = self.send_sms(
            self.phone_number,
            self.message,
            self.recipient_name,
            self.template_id.id if self.template_id else None,
            self.recipient_type,
            self.recipient_id
        )
        
        if result['success']:
            return {'type': 'ir.actions.client', 'tag': 'reload'}
        else:
            return {'warning': {'title': 'Error', 'message': result['error']}}