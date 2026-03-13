from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_data()

def seed_data():
    from models.user import User
    from models.doctor import Doctor
    from models.doctor_availability import DoctorAvailability
    from werkzeug.security import generate_password_hash
    from datetime import time
    
    if User.query.count() == 0:
        receptionist = User(
            name='Sarah Johnson',
            email='receptionist@clinic.com',
            password=generate_password_hash('receptionist123'),
            role='receptionist'
        )
        doctor_user = User(
            name='Dr. Michael Smith',
            email='doctor@clinic.com',
            password=generate_password_hash('doctor123'),
            role='doctor'
        )
        db.session.add(receptionist)
        db.session.add(doctor_user)
        db.session.commit()
        
        doctor = Doctor(
            name='Dr. Michael Smith',
            specialization='General Physician'
        )
        db.session.add(doctor)
        db.session.commit()
        
        # Add default availability (Monday to Friday, 9 AM to 5 PM)
        for day in range(5):  # 0=Monday to 4=Friday
            availability = DoctorAvailability(
                doctor_id=doctor.id,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0),
                is_available=True
            )
            db.session.add(availability)
        db.session.commit()
