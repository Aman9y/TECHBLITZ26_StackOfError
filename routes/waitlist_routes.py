from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from database import db
from models.waitlist import Waitlist
from datetime import datetime

waitlist_bp = Blueprint('waitlist', __name__)

@waitlist_bp.route('/waitlist')
def waitlist_page():
    if 'user_id' not in session or session.get('role') != 'receptionist':
        return redirect(url_for('auth.login'))
    return render_template('waitlist.html')

@waitlist_bp.route('/api/waitlist', methods=['GET'])
def get_waitlist():
    waitlist_entries = Waitlist.query.filter_by(status='waiting').order_by(Waitlist.created_at).all()
    return jsonify([w.to_dict() for w in waitlist_entries])

@waitlist_bp.route('/api/waitlist', methods=['POST'])
def add_to_waitlist():
    data = request.json
    
    waitlist_entry = Waitlist(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        preferred_date=datetime.fromisoformat(data['preferred_date']).date(),
        preferred_time=datetime.fromisoformat(data['preferred_time']).time(),
        status='waiting'
    )
    db.session.add(waitlist_entry)
    db.session.commit()
    
    return jsonify(waitlist_entry.to_dict()), 201

@waitlist_bp.route('/api/waitlist/<int:waitlist_id>', methods=['DELETE'])
def remove_from_waitlist(waitlist_id):
    waitlist_entry = Waitlist.query.get_or_404(waitlist_id)
    db.session.delete(waitlist_entry)
    db.session.commit()
    return '', 204
