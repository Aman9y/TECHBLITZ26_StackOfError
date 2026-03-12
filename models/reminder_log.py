from database import db
from datetime import datetime

class ReminderLog(db.Model):
    __tablename__ = 'reminder_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='sent')
    
    appointment = db.relationship('Appointment', backref='reminder_logs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'message': self.message,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'status': self.status
        }
