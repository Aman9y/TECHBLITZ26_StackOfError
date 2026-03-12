from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from database import db
from models.patient import Patient

patient_bp = Blueprint('patients', __name__)

@patient_bp.route('/patients')
def patients_page():
    if 'user_id' not in session or session.get('role') != 'receptionist':
        return redirect(url_for('auth.login'))
    return render_template('patients.html')

@patient_bp.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients])

@patient_bp.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    patient = Patient(
        name=data['name'],
        phone=data['phone'],
        email=data.get('email', '')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201

@patient_bp.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict())

@patient_bp.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    patient.name = data.get('name', patient.name)
    patient.phone = data.get('phone', patient.phone)
    patient.email = data.get('email', patient.email)
    db.session.commit()
    return jsonify(patient.to_dict())

@patient_bp.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return '', 204
