from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Local JSON file storage paths
DATA_DIR = 'local_data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
DOCTORS_FILE = os.path.join(DATA_DIR, 'doctors.json')
APPOINTMENTS_FILE = os.path.join(DATA_DIR, 'appointments.json')

# Initialize data directory and files
def init_local_storage():
    """Initialize local JSON storage"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Initialize users file
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
    
    # Initialize doctors file with sample data
    if not os.path.exists(DOCTORS_FILE):
        doctors = [
            {
                "doctor_id": "doc-001",
                "name": "Sarah Johnson",
                "specialization": "Cardiology",
                "available_slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
            },
            {
                "doctor_id": "doc-002",
                "name": "Michael Chen",
                "specialization": "Pediatrics",
                "available_slots": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
            },
            {
                "doctor_id": "doc-003",
                "name": "Emily Davis",
                "specialization": "Dermatology",
                "available_slots": ["10:00", "11:00", "14:00", "15:00", "16:00"]
            },
            {
                "doctor_id": "doc-004",
                "name": "Robert Martinez",
                "specialization": "Orthopedics",
                "available_slots": ["09:00", "10:00", "12:00", "14:00", "15:00"]
            },
            {
                "doctor_id": "doc-005",
                "name": "Jennifer Lee",
                "specialization": "General Medicine",
                "available_slots": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]
            }
        ]
        with open(DOCTORS_FILE, 'w') as f:
            json.dump(doctors, f, indent=2)
    
    # Initialize appointments file
    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, 'w') as f:
            json.dump([], f)

# Helper functions for JSON file operations
def read_json_file(filepath):
    """Read data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return []

def write_json_file(filepath, data):
    """Write data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize storage on startup
init_local_storage()


# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@app.route('/signup', methods=['POST'])
def signup():
    """
    User registration endpoint (LOCAL VERSION)
    Expected JSON: {name, email, phone, password}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        email = data['email'].lower().strip()
        
        # Check if email already exists
        users = read_json_file(USERS_FILE)
        if any(user['email'] == email for user in users):
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409
        
        # Generate user ID and hash password
        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash(data['password'], method='pbkdf2:sha256')
        
        # Create new user
        new_user = {
            'user_id': user_id,
            'name': data['name'],
            'email': email,
            'phone': data['phone'],
            'password_hash': password_hash
        }
        
        # Save to file
        users.append(new_user)
        write_json_file(USERS_FILE, users)
        
        print(f"✅ User registered: {email}")
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/login', methods=['POST'])
def login():
    """
    User login endpoint (LOCAL VERSION)
    Expected JSON: {email, password}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        email = data['email'].lower().strip()
        
        # Find user by email
        users = read_json_file(USERS_FILE)
        user = next((u for u in users if u['email'] == email), None)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        # Verify password
        if not check_password_hash(user['password_hash'], data['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        print(f"✅ User logged in: {email}")
        
        return jsonify({
            'success': True,
            'user_id': user['user_id'],
            'name': user['name'],
            'email': user['email'],
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


# ============================================
# DOCTOR MANAGEMENT ENDPOINTS
# ============================================

@app.route('/doctors', methods=['GET'])
def get_doctors():
    """
    Retrieve all doctors (LOCAL VERSION)
    Returns: List of doctors with their details
    """
    try:
        doctors = read_json_file(DOCTORS_FILE)
        
        print(f"✅ Retrieved {len(doctors)} doctors")
        
        return jsonify({
            'success': True,
            'doctors': doctors
        }), 200
        
    except Exception as e:
        print(f"Get doctors error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve doctors'
        }), 500


# ============================================
# APPOINTMENT BOOKING ENDPOINTS
# ============================================

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    """
    Book an appointment (LOCAL VERSION)
    Expected JSON: {user_id, doctor_id, date, time}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'doctor_id', 'date', 'time']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        user_id = data['user_id']
        doctor_id = data['doctor_id']
        appointment_date = data['date']
        appointment_time = data['time']
        
        # Validate user exists
        users = read_json_file(USERS_FILE)
        user = next((u for u in users if u['user_id'] == user_id), None)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Validate doctor exists
        doctors = read_json_file(DOCTORS_FILE)
        doctor = next((d for d in doctors if d['doctor_id'] == doctor_id), None)
        if not doctor:
            return jsonify({
                'success': False,
                'error': 'Doctor not found'
            }), 404
        
        # Check for double booking
        appointments = read_json_file(APPOINTMENTS_FILE)
        existing = next((a for a in appointments 
                        if a['doctor_id'] == doctor_id 
                        and a['date'] == appointment_date 
                        and a['time'] == appointment_time 
                        and a['status'] == 'booked'), None)
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'This time slot is already booked. Please select another time.'
            }), 409
        
        # Create appointment
        appointment_id = str(uuid.uuid4())
        
        new_appointment = {
            'appointment_id': appointment_id,
            'user_id': user_id,
            'doctor_id': doctor_id,
            'date': appointment_date,
            'time': appointment_time,
            'status': 'booked',
            'created_at': datetime.now().isoformat()
        }
        
        # Save appointment
        appointments.append(new_appointment)
        write_json_file(APPOINTMENTS_FILE, appointments)
        
        # Mock SNS notification (just print to console)
        print(f"\n{'='*60}")
        print(f"📧 EMAIL NOTIFICATION (MOCK)")
        print(f"{'='*60}")
        print(f"To: {user['email']}")
        print(f"Subject: Appointment Confirmation - Care_4_U Hospitals")
        print(f"\nDear {user['name']},")
        print(f"\nYour appointment has been confirmed!")
        print(f"\nAppointment Details:")
        print(f"- Doctor: Dr. {doctor['name']}")
        print(f"- Specialization: {doctor['specialization']}")
        print(f"- Date: {appointment_date}")
        print(f"- Time: {appointment_time}")
        print(f"- Appointment ID: {appointment_id}")
        print(f"\nThank you for choosing Care_4_U Hospitals.")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': True,
            'appointment_id': appointment_id,
            'message': 'Appointment booked successfully',
            'details': {
                'doctor_name': doctor['name'],
                'specialization': doctor['specialization'],
                'date': appointment_date,
                'time': appointment_time
            }
        }), 201
        
    except Exception as e:
        print(f"Book appointment error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to book appointment'
        }), 500


# ============================================
# UTILITY ENDPOINTS
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Care_4_U Hospitals API (LOCAL VERSION)',
        'storage': 'JSON Files'
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        'message': 'Welcome to Care_4_U Hospitals API (LOCAL VERSION)',
        'version': '1.0-local',
        'storage': 'JSON Files (local_data/)',
        'endpoints': {
            'POST /signup': 'User registration',
            'POST /login': 'User login',
            'GET /doctors': 'Get all doctors',
            'POST /book-appointment': 'Book an appointment',
            'GET /health': 'Health check'
        }
    }), 200


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏥 Care_4_U Hospitals - LOCAL DEVELOPMENT SERVER")
    print("="*60)
    print("📁 Storage: JSON Files (local_data/)")
    print("🌐 Server: http://localhost:5000")
    print("📧 Email: Mock notifications (console only)")
    print("="*60 + "\n")
    
    # Run on all interfaces so it's accessible from outside
    app.run(host='0.0.0.0', port=5000, debug=True)
