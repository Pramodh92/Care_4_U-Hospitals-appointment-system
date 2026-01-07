from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
from datetime import datetime
import os

import os

# Get the path to the frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')

app = Flask(__name__, 
            static_folder=frontend_dir,
            static_url_path='',
            template_folder=frontend_dir)
CORS(app)

# AWS Configuration - Uses IAM role credentials from EC2
# No hardcoded credentials needed
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')

# DynamoDB Tables
users_table = dynamodb.Table('Care4U_Users')
doctors_table = dynamodb.Table('Care4U_Doctors')
appointments_table = dynamodb.Table('Care4U_Appointments')

# SNS Topic ARN - Update this with your actual SNS topic ARN after creation
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:892485120480:Care4U_Appointments')


# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@app.route('/signup', methods=['POST'])
def signup():
    """
    User registration endpoint
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
        try:
            response = users_table.scan(
                FilterExpression=Attr('email').eq(email)
            )
            if response['Items']:
                return jsonify({
                    'success': False,
                    'error': 'Email already registered'
                }), 409
        except Exception as e:
            print(f"Error checking email: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Database error'
            }), 500
        
        # Generate user ID and hash password
        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash(data['password'], method='pbkdf2:sha256')
        
        # Store user in DynamoDB
        users_table.put_item(
            Item={
                'user_id': user_id,
                'name': data['name'],
                'email': email,
                'phone': data['phone'],
                'password_hash': password_hash
            }
        )
        
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
    User login endpoint
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
        response = users_table.scan(
            FilterExpression=Attr('email').eq(email)
        )
        
        if not response['Items']:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        user = response['Items'][0]
        
        # Verify password
        if not check_password_hash(user['password_hash'], data['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
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
    Retrieve all doctors
    Returns: List of doctors with their details
    """
    try:
        response = doctors_table.scan()
        doctors = response['Items']
        
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
    Book an appointment
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
        try:
            user_response = users_table.get_item(Key={'user_id': user_id})
            if 'Item' not in user_response:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            user = user_response['Item']
        except Exception as e:
            print(f"Error fetching user: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Invalid user'
            }), 400
        
        # Validate doctor exists
        try:
            doctor_response = doctors_table.get_item(Key={'doctor_id': doctor_id})
            if 'Item' not in doctor_response:
                return jsonify({
                    'success': False,
                    'error': 'Doctor not found'
                }), 404
            doctor = doctor_response['Item']
        except Exception as e:
            print(f"Error fetching doctor: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Invalid doctor'
            }), 400
        
        # Check for double booking (same doctor, date, and time)
        try:
            existing_appointments = appointments_table.scan(
                FilterExpression=Attr('doctor_id').eq(doctor_id) & 
                                Attr('date').eq(appointment_date) & 
                                Attr('time').eq(appointment_time) &
                                Attr('status').eq('booked')
            )
            
            if existing_appointments['Items']:
                return jsonify({
                    'success': False,
                    'error': 'This time slot is already booked. Please select another time.'
                }), 409
        except Exception as e:
            print(f"Error checking double booking: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to validate appointment slot'
            }), 500
        
        # Create appointment
        appointment_id = str(uuid.uuid4())
        
        appointments_table.put_item(
            Item={
                'appointment_id': appointment_id,
                'user_id': user_id,
                'doctor_id': doctor_id,
                'date': appointment_date,
                'time': appointment_time,
                'status': 'booked',
                'created_at': datetime.now().isoformat()
            }
        )
        
        # Send SNS notification
        try:
            message = f"""Dear {user['name']},

Your appointment has been confirmed!

Appointment Details:
- Doctor: Dr. {doctor['name']}
- Specialization: {doctor['specialization']}
- Date: {appointment_date}
- Time: {appointment_time}
- Appointment ID: {appointment_id}

Thank you for choosing Care_4_U Hospitals.

Best regards,
Care_4_U Hospitals Team"""

            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject='Appointment Confirmation - Care_4_U Hospitals',
                Message=message
            )
            print(f"SNS notification sent for appointment {appointment_id}")
        except Exception as e:
            # Log error but don't fail the appointment booking
            print(f"SNS notification error: {str(e)}")
        
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
        'service': 'Care_4_U Hospitals API'
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Root endpoint - Serves frontend"""
    return send_from_directory(frontend_dir, 'index.html')


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
    # Run on all interfaces so it's accessible from outside EC2
    app.run(host='0.0.0.0', port=5000, debug=True)
