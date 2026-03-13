from database import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=True)
    duration = db.Column(db.Integer, default=30)
    status = db.Column(db.String(20), default='booked')
    is_followup = db.Column(db.Boolean, default=False)
    parent_appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    followup_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    parent_appointment = db.relationship('Appointment', remote_side=[id], backref='followup_appointments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'patient_phone': self.patient.phone if self.patient else None,
            'date': self.date.isoformat(),
            'time': self.time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'duration': self.duration,
            'status': self.status,
            'is_followup': self.is_followup,
            'parent_appointment_id': self.parent_appointment_id,
            'followup_notes': self.followup_notes,
            'datetime': f"{self.date.isoformat()}T{self.time.strftime('%H:%M:%S')}"
        }
