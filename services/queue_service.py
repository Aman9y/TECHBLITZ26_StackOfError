from database import db
from models.queue import Queue

class QueueService:
    
    @staticmethod
    def checkin_patient(patient_id, appointment_id=None, is_emergency=False, auto_checked_in=False):
        max_position = db.session.query(db.func.max(Queue.position)).filter(
            Queue.status.in_(['waiting', 'in_consultation'])
        ).scalar() or 0
        
        position = 0 if is_emergency else max_position + 1
        
        queue_entry = Queue(
            patient_id=patient_id,
            appointment_id=appointment_id,
            position=position,
            status='waiting',
            is_emergency=is_emergency,
            auto_checked_in=auto_checked_in
        )
        db.session.add(queue_entry)
        db.session.commit()
        
        return queue_entry
    
    @staticmethod
    def get_next_patient():
        return Queue.query.filter_by(status='waiting').order_by(
            Queue.is_emergency.desc(),
            Queue.position
        ).first()
