from database import db
from models.waitlist import Waitlist
from models.appointment import Appointment
from services.reminder_service import ReminderService

class WaitlistService:
    
    @staticmethod
    def process_cancellation(cancelled_appointment):
        waitlist_entries = Waitlist.query.filter_by(
            doctor_id=cancelled_appointment.doctor_id,
            status='waiting'
        ).order_by(Waitlist.created_at).all()
        
        for entry in waitlist_entries:
            if entry.preferred_date == cancelled_appointment.date:
                new_appointment = Appointment(
                    doctor_id=cancelled_appointment.doctor_id,
                    patient_id=entry.patient_id,
                    date=cancelled_appointment.date,
                    time=cancelled_appointment.time,
                    status='booked'
                )
                db.session.add(new_appointment)
                
                entry.status = 'booked'
                db.session.commit()
                
                ReminderService.send_waitlist_notification(entry, new_appointment)
                
                return new_appointment
        
        return None
