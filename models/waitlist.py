from database import db
from datetime import datetime

class Waitlist(db.Model):
    __tablename__ = 'waitlist'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='waiting')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('Patient', backref='waitlist_entries')
    doctor = db.relationship('Doctor', backref='waitlist_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'patient_phone': self.patient.phone if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'preferred_date': self.preferred_date.isoformat(),
            'preferred_time': self.preferred_time.strftime('%H:%M'),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
