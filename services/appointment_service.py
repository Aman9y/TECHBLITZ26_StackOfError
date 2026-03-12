from models.appointment import Appointment
from datetime import datetime, timedelta

class AppointmentService:
    
    @staticmethod
    def check_conflict(doctor_id, date, time, exclude_id=None):
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
        start_time = datetime.combine(date, time)
        
        for i in range(1, 13):
            for delta in [timedelta(minutes=30*i), timedelta(minutes=-30*i)]:
                check_time = start_time + delta
                
                if check_time.date() != date:
                    continue
                
                if not AppointmentService.check_conflict(doctor_id, date, check_time.time()):
                    return {
                        'date': date.isoformat(),
                        'time': check_time.time().strftime('%H:%M')
                    }
        
        next_day = date + timedelta(days=1)
        return {
            'date': next_day.isoformat(),
            'time': '09:00'
        }
