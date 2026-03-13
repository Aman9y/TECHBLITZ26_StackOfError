from flask import Flask
from flask_socketio import SocketIO
from config import Config
from database import init_db
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.appointment_routes import appointment_bp
from routes.queue_routes import queue_bp
from routes.waitlist_routes import waitlist_bp
from scheduler.reminder_scheduler import init_scheduler

app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app, cors_allowed_origins="*")
app.extensions['socketio'] = socketio

init_db(app)

app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(queue_bp)
app.register_blueprint(waitlist_bp)

init_scheduler(app)

# Test endpoint for manual reminder testing
@app.route('/test-reminder/<int:appointment_id>')
def test_reminder(appointment_id):
    from models.appointment import Appointment
    from services.reminder_service import ReminderService
    
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        success = ReminderService.send_appointment_reminder(appointment, 24)
        if success:
            return f"✓ Reminder sent to {appointment.patient.name} at {appointment.patient.phone}"
        else:
            return "✗ Failed to send reminder. Check console for errors."
    return "Appointment not found"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
