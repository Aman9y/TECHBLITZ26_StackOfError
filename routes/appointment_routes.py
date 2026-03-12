from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from database import db
from models.appointment import Appointment
from models.doctor import Doctor
from models.patient import Patient
from services.appointment_service import AppointmentService
from datetime import datetime, date

appointment_bp = Blueprint('appointments', __name__)

@appointment_bp.route('/appointments')
def appointments_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('appointments.html')

@appointment_bp.route('/api/appointments', methods=['GET'])
def get_appointments():
    start = request.args.get('start')
    end = request.args.get('end')
    
    query = Appointment.query
    
    if start:
        start_clean = start.split('T')[0]
        start_date = datetime.strptime(start_clean, '%Y-%m-%d').date()
        query = query.filter(Appointment.date >= start_date)
    
    if end:
        end_clean = end.split('T')[0]
        end_date = datetime.strptime(end_clean, '%Y-%m-%d').date()
        query = query.filter(Appointment.date <= end_date)
    
    appointments = query.all()
    return jsonify([a.to_dict() for a in appointments])

@appointment_bp.route('/api/appointments/today', methods=['GET'])
def get_today_appointments():
    today = date.today()
    appointments = Appointment.query.filter_by(date=today).all()
    return jsonify([a.to_dict() for a in appointments])

@appointment_bp.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    
    appointment_date = datetime.fromisoformat(data['date']).date()
    appointment_time = datetime.fromisoformat(data['time']).time()
    
    conflict = AppointmentService.check_conflict(
        data['doctor_id'],
        appointment_date,
        appointment_time
    )
    
    if conflict:
        available_slot = AppointmentService.find_nearest_slot(
            data['doctor_id'],
            appointment_date,
            appointment_time
        )
        return jsonify({
            'error': 'Slot already booked',
            'suggested_slot': available_slot
        }), 409
    
    appointment = Appointment(
        doctor_id=data['doctor_id'],
        patient_id=data['patient_id'],
        date=appointment_date,
        time=appointment_time,
        status='booked'
    )
    db.session.add(appointment)
    db.session.commit()
    
    return jsonify(appointment.to_dict()), 201

@appointment_bp.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.json
    
    if 'date' in data and 'time' in data:
        new_date = datetime.fromisoformat(data['date']).date()
        new_time = datetime.fromisoformat(data['time']).time()
        
        conflict = AppointmentService.check_conflict(
            appointment.doctor_id,
            new_date,
            new_time,
            exclude_id=appointment_id
        )
        
        if conflict:
            return jsonify({'error': 'Slot already booked'}), 409
        
        appointment.date = new_date
        appointment.time = new_time
    
    if 'status' in data:
        old_status = appointment.status
        appointment.status = data['status']
        
        if old_status != 'cancelled' and data['status'] == 'cancelled':
            from services.waitlist_service import WaitlistService
            WaitlistService.process_cancellation(appointment)
    
    db.session.commit()
    return jsonify(appointment.to_dict())

@appointment_bp.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return '', 204

@appointment_bp.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([d.to_dict() for d in doctors])
