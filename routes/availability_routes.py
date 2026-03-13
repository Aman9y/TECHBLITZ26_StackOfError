from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from database import db
from models.doctor_availability import DoctorAvailability
from models.doctor import Doctor
from datetime import datetime

availability_bp = Blueprint('availability', __name__)

@availability_bp.route('/availability')
def availability_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('availability.html')

@availability_bp.route('/api/availability', methods=['GET'])
def get_availability():
    doctor_id = request.args.get('doctor_id')
    
    query = DoctorAvailability.query
    if doctor_id:
        query = query.filter_by(doctor_id=doctor_id)
    
    availability = query.all()
    return jsonify([a.to_dict() for a in availability])

@availability_bp.route('/api/availability', methods=['POST'])
def create_availability():
    data = request.json
    
    availability = DoctorAvailability(
        doctor_id=data['doctor_id'],
        day_of_week=data['day_of_week'],
        start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
        end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
        is_available=data.get('is_available', True)
    )
    db.session.add(availability)
    db.session.commit()
    
    return jsonify(availability.to_dict()), 201

@availability_bp.route('/api/availability/<int:availability_id>', methods=['PUT'])
def update_availability(availability_id):
    availability = DoctorAvailability.query.get_or_404(availability_id)
    data = request.json
    
    if 'day_of_week' in data:
        availability.day_of_week = data['day_of_week']
    if 'start_time' in data:
        availability.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
    if 'end_time' in data:
        availability.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    if 'is_available' in data:
        availability.is_available = data['is_available']
    
    db.session.commit()
    return jsonify(availability.to_dict())

@availability_bp.route('/api/availability/<int:availability_id>', methods=['DELETE'])
def delete_availability(availability_id):
    availability = DoctorAvailability.query.get_or_404(availability_id)
    db.session.delete(availability)
    db.session.commit()
    return '', 204

@availability_bp.route('/api/doctors/<int:doctor_id>/available-slots', methods=['GET'])
def get_available_slots(doctor_id):
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date required'}), 400
    
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    day_of_week = date.weekday()
    
    availability = DoctorAvailability.query.filter_by(
        doctor_id=doctor_id,
        day_of_week=day_of_week,
        is_available=True
    ).all()
    
    if not availability:
        return jsonify([])
    
    from models.appointment import Appointment
    booked_appointments = Appointment.query.filter_by(
        doctor_id=doctor_id,
        date=date
    ).filter(Appointment.status != 'cancelled').all()
    
    booked_times = [apt.time for apt in booked_appointments]
    
    slots = []
    for avail in availability:
        current_time = datetime.combine(date, avail.start_time)
        end_time = datetime.combine(date, avail.end_time)
        
        while current_time < end_time:
            if current_time.time() not in booked_times:
                slots.append({
                    'time': current_time.strftime('%H:%M'),
                    'available': True
                })
            current_time = datetime.combine(date, current_time.time())
            current_time = current_time.replace(minute=current_time.minute + 30)
    
    return jsonify(slots)
