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
