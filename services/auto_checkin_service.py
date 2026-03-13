from models.appointment import Appointment
from models.queue import Queue
from services.queue_service import QueueService
from datetime import datetime, timedelta, date
from database import db

class AutoCheckinService:
    
    @staticmethod
    def auto_checkin_appointments():
        """Auto check-in patients 15 minutes before their appointment"""
        now = datetime.now()
        today = date.today()
        
        # Get appointments for today that are booked
        appointments = Appointment.query.filter_by(
            date=today,
            status='booked'
        ).all()
        
        for appointment in appointments:
            # Check if already in queue
            existing_queue = Queue.query.filter_by(
                appointment_id=appointment.id
            ).filter(Queue.status.in_(['waiting', 'in_consultation'])).first()
            
            if existing_queue:
                continue
            
            # Calculate appointment time
            appointment_datetime = datetime.combine(appointment.date, appointment.time)
            time_until_appointment = (appointment_datetime - now).total_seconds() / 60
            
            # Auto check-in if within 15 minutes before appointment
            if -5 <= time_until_appointment <= 15:
                print(f"🔔 Auto check-in: {appointment.patient.name} for appointment #{appointment.id}")
                
                queue_entry = QueueService.checkin_patient(
                    appointment.patient_id,
                    appointment.id,
                    is_emergency=False,
                    auto_checked_in=True
                )
                
                # Broadcast to all clients
                try:
                    from flask import current_app
                    socketio = current_app.extensions.get('socketio')
                    if socketio:
                        socketio.emit('queue_updated', {
                            'action': 'AUTO_CHECKED_IN',
                            'data': queue_entry.to_dict()
                        })
                except:
                    pass
