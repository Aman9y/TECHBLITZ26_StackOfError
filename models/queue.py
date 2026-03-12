from database import db
from datetime import datetime

class Queue(db.Model):
    __tablename__ = 'queue'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='waiting')
    is_emergency = db.Column(db.Boolean, default=False)
    checked_in_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('Patient', backref='queue_entries')
    appointment = db.relationship('Appointment', backref='queue_entry')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'appointment_id': self.appointment_id,
            'position': self.position,
            'status': self.status,
            'is_emergency': self.is_emergency,
            'checked_in_at': self.checked_in_at.isoformat() if self.checked_in_at else None
        }
