# Care_4_U Hospitals - AWS Doctor Appointment System

<div align="center">

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?style=for-the-badge&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-green?style=for-the-badge&logo=flask)
![DynamoDB](https://img.shields.io/badge/DynamoDB-Database-blue?style=for-the-badge&logo=amazon-dynamodb)
![SNS](https://img.shields.io/badge/SNS-Notifications-red?style=for-the-badge&logo=amazon-aws)

**A complete, production-ready AWS-based doctor appointment booking system**

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Deployment](#-deployment) • [API Documentation](#-api-documentation)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Care_4_U Hospitals** is a comprehensive, cloud-native doctor appointment booking system built on AWS infrastructure. The system enables patients to:

- Register and authenticate securely
- Browse available doctors by specialization
- Book appointments with real-time availability checking
- Receive instant email notifications via AWS SNS

This project demonstrates **production-grade AWS architecture** and is perfect for:
- 📚 Learning AWS services integration
- 💼 Portfolio/resume projects
- 🎤 Technical interviews
- 🏗️ Real-world deployment scenarios

---

## ✨ Features

### 🔐 User Authentication
- Secure user registration with email validation
- Password hashing using `pbkdf2:sha256`
- Session management with localStorage
- Login/logout functionality

### 👨‍⚕️ Doctor Management
- Browse doctors by specialization
- View doctor availability
- Real-time doctor information display
- Persistent storage in DynamoDB

### 📅 Appointment Booking
- Interactive date and time selection
- **Double-booking prevention** with validation
- Instant booking confirmation
- Appointment history tracking

### 📧 Email Notifications
- Automated email notifications via AWS SNS
- Detailed appointment information
- Confirmation with appointment ID
- Customizable message templates

### 🔒 Security
- IAM role-based access control
- No hardcoded credentials
- Secure password storage
- CORS-enabled API

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Web Browser)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND                                  │
│              (HTML/CSS/JavaScript)                           │
│                                                              │
│  • index.html (Login)                                        │
│  • signup.html (Registration)                                │
│  • dashboard.html (Doctor List)                              │
│  • book.html (Appointment Booking)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ REST API Calls
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND                                   │
│                  (Flask + Python)                            │
│                                                              │
│  Endpoints:                                                  │
│  • POST /signup                                              │
│  • POST /login                                               │
│  • GET  /doctors                                             │
│  • POST /book-appointment                                    │
│                                                              │
│  Hosted on: AWS EC2                                          │
└─────┬──────────────────────────────────────────┬────────────┘
      │                                          │
      │ boto3                                    │ boto3
      ▼                                          ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│     AWS DynamoDB         │      │       AWS SNS            │
│                          │      │                          │
│  Tables:                 │      │  Topic:                  │
│  • Care4U_Users          │      │  • Care4U_Appointments   │
│  • Care4U_Doctors        │      │                          │
│  • Care4U_Appointments   │      │  Subscriptions:          │
│                          │      │  • Email                 │
└──────────────────────────┘      └──────────────────────────┘
           ▲                                   │
           │                                   │
           │ IAM Role                          │ Email
           │ (Care4U_EC2_Role)                 ▼
           │                          ┌─────────────────┐
           └──────────────────────────│  USER EMAIL     │
                                      └─────────────────┘
```

### Data Flow

1. **User Registration/Login**
   - Frontend sends credentials to Flask backend
   - Backend validates and stores in DynamoDB
   - Returns authentication token

2. **Doctor Browsing**
   - Frontend requests doctor list
   - Backend queries DynamoDB Doctors table
   - Returns doctor information with specializations

3. **Appointment Booking**
   - User selects doctor, date, and time
   - Backend validates availability (prevents double booking)
   - Stores appointment in DynamoDB
   - Triggers SNS notification
   - User receives email confirmation

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Structure and content
- **CSS3** - Styling with modern design
- **Vanilla JavaScript** - Client-side logic and API calls
- **Fetch API** - Asynchronous HTTP requests

### Backend
- **Python 3.9+** - Programming language
- **Flask 3.0** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Werkzeug** - Password hashing and security
- **boto3** - AWS SDK for Python

### AWS Services
- **EC2** - Application hosting (Amazon Linux 2023)
- **DynamoDB** - NoSQL database for data storage
- **SNS** - Email notification service
- **IAM** - Identity and access management

---

## 📁 Project Structure

```
care4u-hospitals/
│
├── backend/
│   ├── app.py                 # Flask application with REST APIs
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html            # Login page
│   ├── signup.html           # User registration page
│   ├── dashboard.html        # Doctor listing page
│   ├── book.html             # Appointment booking page
│   ├── style.css             # Global styles
│   └── script.js             # JavaScript utilities and API calls
│
├── DEPLOYMENT.md             # Step-by-step AWS deployment guide
└── README.md                 # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- AWS Account
- Git (optional)

### Local Development Setup

1. **Clone or Download the Project**

```bash
git clone <repository-url>
cd care4u-hospitals
```

2. **Install Backend Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

3. **Configure AWS Credentials (for local testing)**

```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

4. **Update Configuration**

Edit `backend/app.py`:
- Set your SNS Topic ARN
- Verify DynamoDB region

Edit `frontend/script.js`:
- Set `API_BASE_URL` to `http://localhost:5000`

5. **Run Backend Locally**

```bash
cd backend
python app.py
```

Backend will run on: `http://localhost:5000`

6. **Run Frontend Locally**

```bash
cd frontend
python -m http.server 8000
```

Frontend will run on: `http://localhost:8000`

---

## 🌐 Deployment

For complete AWS deployment instructions, see **[DEPLOYMENT.md](DEPLOYMENT.md)**

### Quick Deployment Overview

1. **Create IAM Role** with DynamoDB and SNS permissions
2. **Create DynamoDB Tables** (Users, Doctors, Appointments)
3. **Seed Doctor Data** in DynamoDB
4. **Create SNS Topic** and confirm email subscription
5. **Launch EC2 Instance** with IAM role attached
6. **Deploy Backend** (Flask application)
7. **Deploy Frontend** (HTML/CSS/JS files)
8. **Test End-to-End** functionality

**Estimated Deployment Time:** 30-45 minutes

---

## 📡 API Documentation

### Base URL
```
http://YOUR_EC2_PUBLIC_IP:5000
```

### Endpoints

#### 1. User Registration

**POST** `/signup`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "password": "securepassword"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "user_id": "uuid-string",
  "message": "User registered successfully"
}
```

**Error Response (409):**
```json
{
  "success": false,
  "error": "Email already registered"
}
```

---

#### 2. User Login

**POST** `/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "user_id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Login successful"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "Invalid email or password"
}
```

---

#### 3. Get All Doctors

**GET** `/doctors`

**Success Response (200):**
```json
{
  "success": true,
  "doctors": [
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
    }
  ]
}
```

---

#### 4. Book Appointment

**POST** `/book-appointment`

**Request Body:**
```json
{
  "user_id": "uuid-string",
  "doctor_id": "doc-001",
  "date": "2026-01-15",
  "time": "10:00"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "appointment_id": "uuid-string",
  "message": "Appointment booked successfully",
  "details": {
    "doctor_name": "Sarah Johnson",
    "specialization": "Cardiology",
    "date": "2026-01-15",
    "time": "10:00"
  }
}
```

**Error Response (409):**
```json
{
  "success": false,
  "error": "This time slot is already booked. Please select another time."
}
```

---

#### 5. Health Check

**GET** `/health`

**Success Response (200):**
```json
{
  "status": "healthy",
  "service": "Care_4_U Hospitals API"
}
```

---

## 🗄️ Database Schema

### Users Table (`Care4U_Users`)

| Attribute | Type | Description |
|-----------|------|-------------|
| `user_id` | String (PK) | Unique user identifier (UUID) |
| `name` | String | User's full name |
| `email` | String | Email address (unique) |
| `phone` | String | Phone number |
| `password_hash` | String | Hashed password (pbkdf2:sha256) |

---

### Doctors Table (`Care4U_Doctors`)

| Attribute | Type | Description |
|-----------|------|-------------|
| `doctor_id` | String (PK) | Unique doctor identifier |
| `name` | String | Doctor's name |
| `specialization` | String | Medical specialization |
| `available_slots` | List | Available time slots |

---

### Appointments Table (`Care4U_Appointments`)

| Attribute | Type | Description |
|-----------|------|-------------|
| `appointment_id` | String (PK) | Unique appointment identifier (UUID) |
| `user_id` | String | Reference to user |
| `doctor_id` | String | Reference to doctor |
| `date` | String | Appointment date (YYYY-MM-DD) |
| `time` | String | Appointment time (HH:MM) |
| `status` | String | Appointment status (booked/cancelled) |
| `created_at` | String | Timestamp (ISO format) |

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] **User Registration**
  - [ ] Valid registration succeeds
  - [ ] Duplicate email is rejected
  - [ ] Password is hashed in DynamoDB
  
- [ ] **User Login**
  - [ ] Valid credentials succeed
  - [ ] Invalid credentials fail
  - [ ] Session persists across pages
  
- [ ] **Doctor Listing**
  - [ ] All doctors are displayed
  - [ ] Specializations are correct
  
- [ ] **Appointment Booking**
  - [ ] Valid booking succeeds
  - [ ] Double booking is prevented
  - [ ] Confirmation modal appears
  - [ ] Email notification is received
  
- [ ] **Data Persistence**
  - [ ] User data in DynamoDB
  - [ ] Appointment data in DynamoDB
  - [ ] Data survives page refresh

### API Testing with cURL

```bash
# Test signup
curl -X POST http://YOUR_IP:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"1234567890","password":"test123"}'

# Test login
curl -X POST http://YOUR_IP:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Test get doctors
curl http://YOUR_IP:5000/doctors

# Test book appointment
curl -X POST http://YOUR_IP:5000/book-appointment \
  -H "Content-Type: application/json" \
  -d '{"user_id":"USER_ID","doctor_id":"doc-001","date":"2026-01-15","time":"10:00"}'
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Cannot Access Application

**Symptoms:** Browser shows "Cannot connect"

**Solutions:**
- Verify EC2 instance is running
- Check security group allows ports 80, 5000
- Confirm public IP is correct
- Verify Flask is running: `ps aux | grep app.py`

---

#### 2. DynamoDB Access Denied

**Symptoms:** 500 error when accessing API

**Solutions:**
- Verify IAM role is attached to EC2
- Check IAM policies include DynamoDB permissions
- Ensure table names match exactly
- Verify AWS region in code

---

#### 3. Email Notifications Not Received

**Symptoms:** Booking succeeds but no email

**Solutions:**
- Confirm SNS subscription in AWS Console
- Check spam/junk folder
- Verify SNS Topic ARN in `app.py`
- Test SNS manually in AWS Console

---

#### 4. CORS Errors

**Symptoms:** Browser console shows CORS error

**Solutions:**
- Verify Flask-CORS is installed
- Check `CORS(app)` is in `app.py`
- Ensure frontend and backend URLs are correct

---

#### 5. Double Booking Still Occurs

**Symptoms:** Same slot can be booked twice

**Solutions:**
- Check appointment validation logic
- Verify DynamoDB scan filters
- Test with different time slots
- Check appointment status field

---

## 💡 Interview Questions & Answers

### Q1: How does the system prevent double booking?

**Answer:** Before creating an appointment, the backend performs a DynamoDB scan with filters for:
- Same `doctor_id`
- Same `date`
- Same `time`
- Status = `booked`

If any matching appointment exists, the booking is rejected with a 409 error.

---

### Q2: Why use IAM roles instead of access keys?

**Answer:** IAM roles provide:
- **Security:** No hardcoded credentials in code
- **Automatic rotation:** Temporary credentials
- **Least privilege:** Scoped permissions
- **Audit trail:** CloudTrail logging

---

### Q3: How would you scale this system?

**Answer:**
- **Load Balancer:** Distribute traffic across multiple EC2 instances
- **Auto Scaling:** Automatically add/remove instances based on demand
- **DynamoDB Auto Scaling:** Adjust read/write capacity
- **ElastiCache:** Cache doctor data to reduce DynamoDB reads
- **CloudFront:** CDN for frontend static files

---

### Q4: What security improvements would you add?

**Answer:**
- **HTTPS:** SSL/TLS certificates via AWS Certificate Manager
- **JWT Tokens:** Replace localStorage with secure tokens
- **Rate Limiting:** Prevent brute force attacks
- **Input Validation:** Server-side validation for all inputs
- **Secrets Manager:** Store SNS ARN and sensitive config
- **WAF:** Web Application Firewall for DDoS protection

---

## 📊 Cost Estimation

### AWS Free Tier (First 12 Months)

| Service | Free Tier Limit | Estimated Monthly Cost |
|---------|----------------|----------------------|
| EC2 (t2.micro) | 750 hours/month | $0 |
| DynamoDB | 25 GB storage | $0 |
| SNS | 1,000 emails/month | $0 |
| Data Transfer | 15 GB/month | $0 |

**Total:** $0/month (within Free Tier limits)

### After Free Tier

| Service | Usage | Estimated Cost |
|---------|-------|---------------|
| EC2 (t2.micro) | 730 hours/month | ~$8.50 |
| DynamoDB | 25 GB + 10M reads | ~$2.50 |
| SNS | 1,000 emails | ~$2.00 |

**Total:** ~$13/month

---

## 🎓 Learning Outcomes

By completing this project, you will learn:

- ✅ AWS IAM roles and policies
- ✅ DynamoDB table design and operations
- ✅ SNS topic creation and subscriptions
- ✅ EC2 instance configuration and deployment
- ✅ Flask REST API development
- ✅ Frontend-backend integration
- ✅ Security best practices (password hashing, IAM)
- ✅ Error handling and validation
- ✅ Cloud architecture design
- ✅ Production deployment workflow

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- AWS Documentation
- Flask Documentation
- boto3 Documentation
- DynamoDB Best Practices
- SNS Email Notification Guide

---

## 📞 Support

For questions or issues:

1. Check [Troubleshooting](#-troubleshooting) section
2. Review [DEPLOYMENT.md](DEPLOYMENT.md)
3. Open an issue on GitHub
4. Contact: [your-email@example.com]

---

## 🎉 Project Status

✅ **Production Ready**
✅ **Fully Documented**
✅ **Resume Ready**
✅ **Interview Explainable**

---

<div align="center">

**Built with ❤️ using AWS, Python, and Flask**

⭐ Star this repo if you found it helpful!

</div>
