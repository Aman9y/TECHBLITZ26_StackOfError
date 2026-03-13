from models.appointment import Appointment
from models.doctor_availability import DoctorAvailability
from datetime import datetime, timedelta

class AppointmentService:
    
    @staticmethod
    def check_availability(doctor_id, date, time):
        """Check if doctor is available on this day and time"""
        day_of_week = date.weekday()
        
        availability = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            is_available=True
        ).first()
        
        if not availability:
            return False
        
        if time < availability.start_time or time >= availability.end_time:
            return False
        
        return True
    
    @staticmethod
    def check_conflict(doctor_id, date, time, exclude_id=None):
        if not AppointmentService.check_availability(doctor_id, date, time):
            return True
        
        query = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=date,
            time=time
        ).filter(Appointment.status != 'cancelled')
        
        if exclude_id:
            query = query.filter(Appointment.id != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def find_nearest_slot(doctor_id, date, time):
        from models.doctor_availability import DoctorAvailability
        
        start_time = datetime.combine(date, time)
        
        for i in range(1, 13):
            for delta in [timedelta(minutes=30*i), timedelta(minutes=-30*i)]:
                check_time = start_time + delta
                
                if check_time.date() != date:
                    continue
                
                day_of_week = check_time.date().weekday()
                availability = DoctorAvailability.query.filter_by(
                    doctor_id=doctor_id,
                    day_of_week=day_of_week,
                    is_available=True
                ).first()
                
                if not availability:
                    continue
                
                if check_time.time() < availability.start_time or check_time.time() >= availability.end_time:
                    continue
                
                if not AppointmentService.check_conflict(doctor_id, date, check_time.time()):
                    return {
                        'date': date.isoformat(),
                        'time': check_time.time().strftime('%H:%M')
                    }
        
        for next_days in range(1, 8):
            next_day = date + timedelta(days=next_days)
            day_of_week = next_day.weekday()
            
            availability = DoctorAvailability.query.filter_by(
                doctor_id=doctor_id,
                day_of_week=day_of_week,
                is_available=True
            ).first()
            
            if availability:
                return {
                    'date': next_day.isoformat(),
                    'time': availability.start_time.strftime('%H:%M')
                }
        
        return {
            'date': (date + timedelta(days=1)).isoformat(),
            'time': '09:00'
        }
