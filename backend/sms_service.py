"""
SMS Notification Service for Traffic Violations
Sends penalty alerts to vehicle owners via SMS
"""

import os
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️ Twilio not installed - SMS service will run in demo mode")
from datetime import datetime

class SMSNotificationService:
    """
    Sends SMS notifications for traffic violations
    
    Uses Twilio API for SMS delivery
    """
    
    def __init__(self):
        # Twilio credentials (set these as environment variables)
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'YOUR_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'YOUR_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER', '+1234567890')
        
        # Initialize Twilio client
        if not TWILIO_AVAILABLE:
            print("⚠️ SMS service in DEMO mode (install twilio to enable)")
            self.enabled = False
        elif self.account_sid != 'YOUR_ACCOUNT_SID':
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.enabled = True
                print("✅ SMS service initialized (Twilio)")
            except Exception as e:
                print(f"⚠️ SMS service disabled: {e}")
                self.enabled = False
        else:
            print("⚠️ SMS service in DEMO mode (set Twilio credentials to enable)")
            self.enabled = False
    
    def send_violation_sms(self, phone_number, license_plate, violations, total_penalty):
        """
        Send SMS notification for traffic violation
        
        Args:
            phone_number: Driver's phone number
            license_plate: Vehicle number plate
            violations: List of violation objects
            total_penalty: Total penalty amount
            
        Returns:
            dict: SMS send status
        """
        if not self.enabled:
            return {
                'success': False,
                'status': 'demo_mode',
                'message': 'SMS service in demo mode. Set Twilio credentials to send real SMS.'
            }
        
        # Format violation message
        violation_list = '\n'.join([
            f"• {v['name']} - {v['penalty']}"
            for v in violations
        ])
        
        message_body = f"""🚨 TRAFFIC VIOLATION ALERT

Vehicle: {license_plate}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

VIOLATIONS DETECTED:
{violation_list}

TOTAL PENALTY: {total_penalty}

Section: Motor Vehicles Act, 1988

⚠️ Please pay the fine within 30 days to avoid additional charges.

Payment: Visit nearest RTO or online portal.

- Traffic Police Department"""
        
        try:
            # Send SMS via Twilio
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=phone_number
            )
            
            return {
                'success': True,
                'status': 'sent',
                'message_sid': message.sid,
                'to': phone_number
            }
        
        except Exception as e:
            print(f"❌ SMS send failed: {e}")
            return {
                'success': False,
                'status': 'failed',
                'error': str(e)
            }
    
    def send_demo_notification(self, phone_number, license_plate, violations, total_penalty):
        """
        Demo mode notification (logs instead of sending)
        """
        violation_list = ', '.join([v['name'] for v in violations])
        
        print("\n" + "="*60)
        print("📱 DEMO SMS NOTIFICATION")
        print("="*60)
        print(f"To: {phone_number}")
        print(f"Vehicle: {license_plate}")
        print(f"Violations: {violation_list}")
        print(f"Total Penalty: {total_penalty}")
        print("="*60 + "\n")
        
        return {
            'success': True,
            'status': 'demo',
            'message': 'SMS logged (demo mode)'
        }

# Initialize global SMS service
sms_service = SMSNotificationService()
