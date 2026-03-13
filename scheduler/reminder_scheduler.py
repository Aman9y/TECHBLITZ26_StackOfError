from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
from models.appointment import Appointment
from models.reminder_log import ReminderLog
from services.reminder_service import ReminderService
from services.auto_checkin_service import AutoCheckinService
from database import db

def check_and_send_reminders():
    with scheduler.app.app_context():
        now = datetime.now()
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        # Send 24-hour reminders for tomorrow's appointments
        appointments_24h = Appointment.query.filter(
            Appointment.date == tomorrow,
            Appointment.status == 'booked'
        ).all()
        
        for appointment in appointments_24h:
            existing_log = ReminderLog.query.filter_by(
                appointment_id=appointment.id
            ).filter(
                ReminderLog.message.like('%tomorrow%')
            ).first()
            
            if not existing_log:
                print(f"Sending 24h reminder for appointment #{appointment.id}")
                ReminderService.send_appointment_reminder(appointment, 24)
        
        # Send 2-hour reminders for today's appointments
        appointments_2h = Appointment.query.filter(
            Appointment.date == today,
            Appointment.status == 'booked'
        ).all()
        
        for appointment in appointments_2h:
            appointment_datetime = datetime.combine(appointment.date, appointment.time)
            time_diff = (appointment_datetime - now).total_seconds() / 3600
            
            # Send if between 1.5 and 2.5 hours away
            if 1.5 <= time_diff <= 2.5:
                existing_log = ReminderLog.query.filter_by(
                    appointment_id=appointment.id
                ).filter(
                    ReminderLog.message.like('%2 hours%')
                ).first()
                
                if not existing_log:
                    print(f"Sending 2h reminder for appointment #{appointment.id}")
                    ReminderService.send_appointment_reminder(appointment, 2)
        
        # Auto check-in patients
        AutoCheckinService.auto_checkin_appointments()
        
        print(f"[{now.strftime('%H:%M:%S')}] Reminder check completed")

scheduler = BackgroundScheduler()
scheduler_started = False

def init_scheduler(app):
    global scheduler_started
    if scheduler_started:
        return
    
    scheduler.app = app
    scheduler.add_job(func=check_and_send_reminders, trigger="interval", minutes=1)
    scheduler.start()
    scheduler_started = True
    print("✓ Reminder & Auto Check-in scheduler started (runs every 1 minute)")
