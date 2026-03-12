# SmartClinic OS

A complete mini operating system for managing a small doctor's clinic with appointments, queues, and patient management.

## Features

- **Role-Based Access Control**: Separate dashboards for Receptionist and Doctor
- **Appointment Calendar**: Interactive calendar with drag-and-drop rescheduling
- **Real-Time Queue Management**: Live updates using WebSockets
- **Smart Waitlist**: Automatic appointment booking when slots open up
- **WhatsApp Reminders**: Automated reminders 24h and 2h before appointments
- **Patient Management**: Complete CRUD operations for patient records

## Tech Stack

- **Frontend**: HTML, CSS, Bootstrap 5, Vanilla JavaScript, FullCalendar.js
- **Backend**: Python Flask, Flask-SocketIO
- **Database**: SQLite
- **Real-Time**: WebSockets (Socket.IO)
- **Automation**: APScheduler
- **Messaging**: Twilio WhatsApp API

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to project directory**
   ```bash
   cd smartclinic
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Add your Twilio credentials (optional for demo)
   ```bash
   copy .env.example .env
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open browser and go to: `http://localhost:5000`

## Default Login Credentials

### Receptionist
- Email: `receptionist@clinic.com`
- Password: `receptionist123`

### Doctor
- Email: `doctor@clinic.com`
- Password: `doctor123`

## Project Structure

```
smartclinic/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # Database initialization
│
├── models/                     # Database models
│   ├── user.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   ├── queue.py
│   ├── waitlist.py
│   └── reminder_log.py
│
├── routes/                     # API routes
│   ├── auth_routes.py
│   ├── patient_routes.py
│   ├── appointment_routes.py
│   ├── queue_routes.py
│   └── waitlist_routes.py
│
├── services/                   # Business logic
│   ├── reminder_service.py
│   ├── queue_service.py
│   ├── waitlist_service.py
│   └── appointment_service.py
│
├── scheduler/                  # Background jobs
│   └── reminder_scheduler.py
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── receptionist_dashboard.html
│   ├── doctor_dashboard.html
│   ├── appointments.html
│   ├── patients.html
│   ├── queue.html
│   └── waitlist.html
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│
└── requirements.txt            # Python dependencies
```

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /logout` - Logout user

### Patients
- `GET /api/patients` - Get all patients
- `POST /api/patients` - Create patient
- `PUT /api/patients/<id>` - Update patient
- `DELETE /api/patients/<id>` - Delete patient

### Appointments
- `GET /api/appointments` - Get appointments
- `POST /api/appointments` - Create appointment
- `PUT /api/appointments/<id>` - Update appointment
- `DELETE /api/appointments/<id>` - Delete appointment

### Queue
- `GET /api/queue` - Get current queue
- `POST /api/queue/checkin` - Check-in patient
- `POST /api/queue/<id>/call` - Call patient
- `POST /api/queue/<id>/complete` - Complete consultation
- `PUT /api/queue/<id>/emergency` - Mark as emergency

### Waitlist
- `GET /api/waitlist` - Get waitlist
- `POST /api/waitlist` - Add to waitlist
- `DELETE /api/waitlist/<id>` - Remove from waitlist

## WebSocket Events

- `PATIENT_CHECKED_IN` - Patient added to queue
- `PATIENT_CALLED` - Patient called for consultation
- `CONSULTATION_COMPLETED` - Consultation completed
- `QUEUE_UPDATED` - Queue order changed

## Features in Detail

### 1. Appointment Calendar
- Interactive FullCalendar with daily/weekly/monthly views
- Drag-and-drop to reschedule appointments
- Click empty slot to create new appointment
- Color-coded by status (booked, completed, cancelled)
- Conflict detection with suggested alternative slots

### 2. Real-Time Queue
- Live queue updates via WebSockets
- Check-in patients from appointments or walk-ins
- Emergency priority marking
- Doctor can call next patient
- Mark consultations as completed

### 3. Smart Waitlist
- Add patients when slots are full
- Automatic booking when appointments are cancelled
- Matches preferred date/time with available slots
- Automatic WhatsApp notification to patient

### 4. Automated Reminders
- Background job runs every hour
- Sends reminders 24 hours before appointment
- Sends reminders 2 hours before appointment
- Uses Twilio WhatsApp API
- Logs all sent messages

### 5. Role-Based Dashboards

**Receptionist Dashboard:**
- Today's appointments count
- Waiting patients count
- Completed visits count
- Waitlist count
- Today's schedule
- Current queue preview

**Doctor Dashboard:**
- Appointments today count
- Waiting patients count
- Completed consultations count
- Next patient card with call button
- Today's schedule
- Full queue with complete buttons

## Twilio WhatsApp Setup (Optional)

1. Create a Twilio account at https://www.twilio.com
2. Get your Account SID and Auth Token
3. Enable WhatsApp sandbox or get approved WhatsApp number
4. Update `.env` file with credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ```

**Note**: Without Twilio credentials, the app will still work but reminders will only be logged to console.

## Database Schema

### Users
- id, name, email, password, role

### Doctors
- id, name, specialization

### Patients
- id, name, phone, email

### Appointments
- id, doctor_id, patient_id, date, time, status

### Queue
- id, patient_id, appointment_id, position, status, is_emergency

### Waitlist
- id, patient_id, doctor_id, preferred_date, preferred_time, status

### ReminderLogs
- id, appointment_id, message, sent_at, status

## Troubleshooting

### Port already in use
If port 5000 is already in use, modify `app.py`:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

### Database not created
Delete `smartclinic.db` if it exists and restart the application.

### WebSocket not connecting
Ensure you're using `http://` not `https://` for local development.

## Demo Workflow

1. **Login as Receptionist**
   - Email: receptionist@clinic.com
   - Password: receptionist123

2. **Add a Patient**
   - Go to Patients page
   - Click "Add Patient"
   - Fill in details

3. **Create Appointment**
   - Go to Appointments page
   - Click on calendar slot
   - Select patient and doctor
   - Save appointment

4. **Check-in Patient**
   - Go to Queue page
   - Click "Check-in Patient"
   - Select patient and appointment
   - Patient appears in queue

5. **Login as Doctor**
   - Logout and login with doctor credentials
   - Email: doctor@clinic.com
   - Password: doctor123

6. **Call Next Patient**
   - View queue on dashboard
   - Click "Call Next Patient"
   - Patient moves to "In Consultation"

7. **Complete Consultation**
   - Click "Complete" button
   - Appointment marked as completed

## License

MIT License - Free for hackathon and educational use.

## Support

For issues or questions, please create an issue in the repository.
