from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'receptionist':
            return redirect(url_for('auth.receptionist_dashboard'))
        elif session.get('role') == 'doctor':
            return redirect(url_for('auth.doctor_dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            
            if user.role == 'receptionist':
                return redirect(url_for('auth.receptionist_dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('auth.doctor_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        from werkzeug.security import generate_password_hash
        from database import db
        from models.doctor import Doctor
        
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        specialization = request.form.get('specialization', '')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        
        # If registering as doctor, create doctor profile
        if role == 'doctor':
            doctor = Doctor(
                name=name,
                specialization=specialization or 'General Physician'
            )
            db.session.add(doctor)
            db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/receptionist-dashboard')
def receptionist_dashboard():
    if 'user_id' not in session or session.get('role') != 'receptionist':
        return redirect(url_for('auth.login'))
    return render_template('receptionist_dashboard.html')

@auth_bp.route('/doctor-dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('auth.login'))
    return render_template('doctor_dashboard.html')
