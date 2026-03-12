from twilio.rest import Client
from config import Config
from models.reminder_log import ReminderLog
from database import db
from datetime import datetime

class ReminderService:
    
    @staticmethod
    def send_whatsapp_message(to_phone, message):
        print(f"\n📱 Attempting to send WhatsApp to: {to_phone}")
        
        if not Config.TWILIO_ACCOUNT_SID or not Config.TWILIO_AUTH_TOKEN:
            print(f"\n{'='*60}")
            print("⚠️  Twilio not configured. Reminder logged to console only.")
            print(f"{'='*60}")
            print(f"TO: {to_phone}")
            print(f"MESSAGE:\n{message}")
            print(f"{'='*60}\n")
            return True
        
        try:
            client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            
            if not to_phone.startswith('whatsapp:'):
                to_phone = f'whatsapp:{to_phone}'
            
            print(f"📤 Sending to: {to_phone}")
            
            msg = client.messages.create(
                from_=Config.TWILIO_WHATSAPP_FROM,
                body=message,
                to=to_phone
            )
            print(f"✅ WhatsApp sent successfully! SID: {msg.sid}")
            print(f"   Status: {msg.status}")
            print(f"   To: {msg.to}")
            return True
        except Exception as e:
            print(f"❌ Error sending WhatsApp message: {e}")
            return False
    
    @staticmethod
    def send_appointment_reminder(appointment, hours_before):
        patient = appointment.patient
        doctor = appointment.doctor
        
        time_str = appointment.time.strftime('%I:%M %p')
        date_str = appointment.date.strftime('%B %d, %Y')
        
        if hours_before == 24:
            message = f"Hello {patient.name},\n\nReminder: Your appointment with {doctor.name} is tomorrow at {time_str}.\n\nSmartClinic OS"
        else:
            message = f"Hello {patient.name},\n\nReminder: Your appointment with {doctor.name} is in 2 hours at {time_str}.\n\nSmartClinic OS"
        
        success = ReminderService.send_whatsapp_message(patient.phone, message)
        
        log = ReminderLog(
            appointment_id=appointment.id,
            message=message,
            status='sent' if success else 'failed'
        )
        db.session.add(log)
        db.session.commit()
        
        return success
    
    @staticmethod
    def send_waitlist_notification(waitlist_entry, new_appointment):
        patient = waitlist_entry.patient
        doctor = waitlist_entry.doctor
        
        time_str = new_appointment.time.strftime('%I:%M %p')
        date_str = new_appointment.date.strftime('%B %d, %Y')
        
        message = f"Good news {patient.name}!\n\nA slot has opened up with {doctor.name} on {date_str} at {time_str}. Your appointment has been automatically booked.\n\nSmartClinic OS"
        
        ReminderService.send_whatsapp_message(patient.phone, message)
