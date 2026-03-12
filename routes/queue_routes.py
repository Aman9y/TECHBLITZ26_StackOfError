from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from database import db
from models.queue import Queue
from services.queue_service import QueueService

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/queue')
def queue_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('queue.html')

@queue_bp.route('/api/queue', methods=['GET'])
def get_queue():
    queue_entries = Queue.query.filter(
        Queue.status.in_(['waiting', 'in_consultation'])
    ).order_by(Queue.is_emergency.desc(), Queue.position).all()
    return jsonify([q.to_dict() for q in queue_entries])

@queue_bp.route('/api/queue/checkin', methods=['POST'])
def checkin_patient():
    data = request.json
    queue_entry = QueueService.checkin_patient(
        data['patient_id'],
        data.get('appointment_id'),
        data.get('is_emergency', False)
    )
    
    from app import socketio
    socketio.emit('queue_updated', {'action': 'PATIENT_CHECKED_IN', 'data': queue_entry.to_dict()})
    
    return jsonify(queue_entry.to_dict()), 201

@queue_bp.route('/api/queue/<int:queue_id>/call', methods=['POST'])
def call_patient(queue_id):
    queue_entry = Queue.query.get_or_404(queue_id)
    queue_entry.status = 'in_consultation'
    db.session.commit()
    
    from app import socketio
    socketio.emit('queue_updated', {'action': 'PATIENT_CALLED', 'data': queue_entry.to_dict()})
    
    return jsonify(queue_entry.to_dict())

@queue_bp.route('/api/queue/<int:queue_id>/complete', methods=['POST'])
def complete_consultation(queue_id):
    queue_entry = Queue.query.get_or_404(queue_id)
    queue_entry.status = 'completed'
    
    if queue_entry.appointment_id:
        from models.appointment import Appointment
        appointment = Appointment.query.get(queue_entry.appointment_id)
        if appointment:
            appointment.status = 'completed'
    
    db.session.commit()
    
    from app import socketio
    socketio.emit('queue_updated', {'action': 'CONSULTATION_COMPLETED', 'data': queue_entry.to_dict()})
    
    return jsonify(queue_entry.to_dict())

@queue_bp.route('/api/queue/<int:queue_id>/reorder', methods=['PUT'])
def reorder_queue(queue_id):
    data = request.json
    queue_entry = Queue.query.get_or_404(queue_id)
    queue_entry.position = data['position']
    db.session.commit()
    
    from app import socketio
    socketio.emit('queue_updated', {'action': 'QUEUE_REORDERED'})
    
    return jsonify(queue_entry.to_dict())

@queue_bp.route('/api/queue/<int:queue_id>/emergency', methods=['PUT'])
def mark_emergency(queue_id):
    queue_entry = Queue.query.get_or_404(queue_id)
    queue_entry.is_emergency = True
    queue_entry.position = 0
    db.session.commit()
    
    from app import socketio
    socketio.emit('queue_updated', {'action': 'EMERGENCY_MARKED', 'data': queue_entry.to_dict()})
    
    return jsonify(queue_entry.to_dict())
