# 🚀 Quick Start Guide - Care_4_U Hospitals

**Deploy in 30 minutes using AWS Console only!**

---

## 📋 What You'll Create

- ✅ IAM Role for EC2
- ✅ 3 DynamoDB Tables (Users, Doctors, Appointments)
- ✅ SNS Topic for email notifications
- ✅ EC2 Instance running the application

---

## 🎯 Prerequisites

- AWS Account (Free Tier eligible)
- Email address for notifications
- Web browser

---

## 🔥 5-Step Deployment

### Step 1: Create IAM Role (5 mins)

**Console:** IAM → Roles → Create role

1. **Trusted entity:** AWS service → EC2
2. **Create two policies** (Policies → Create policy → JSON):

**DynamoDB Policy** (`Care4U_DynamoDB_Policy`):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:Scan", "dynamodb:Query", "dynamodb:UpdateItem"],
    "Resource": [
      "arn:aws:dynamodb:*:*:table/Care4U_Users",
      "arn:aws:dynamodb:*:*:table/Care4U_Doctors",
      "arn:aws:dynamodb:*:*:table/Care4U_Appointments"
    ]
  }]
}
```

**SNS Policy** (`Care4U_SNS_Policy`):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["sns:Publish"],
    "Resource": "arn:aws:sns:*:*:Care4U_Appointments"
  }]
}
```

3. **Create role** named `Care4U_EC2_Role` with both policies attached

---

### Step 2: Create DynamoDB Tables (5 mins)

**Console:** DynamoDB → Tables → Create table

Create **3 tables** with these settings:

| Table Name | Partition Key | Type |
|------------|---------------|------|
| `Care4U_Users` | `user_id` | String |
| `Care4U_Doctors` | `doctor_id` | String |
| `Care4U_Appointments` | `appointment_id` | String |

**Settings:** Use default settings for all tables

> [!IMPORTANT]
> **Leave tables empty!** Doctor data will auto-populate when you run the app.

---

### Step 3: Create SNS Topic (3 mins)

**Console:** SNS → Topics → Create topic

1. **Type:** Standard
2. **Name:** `Care4U_Appointments`
3. **Create subscription:**
   - Protocol: Email
   - Endpoint: Your email address
4. **Confirm subscription** via email link
5. **Copy the Topic ARN** (you'll need this)

---

### Step 4: Launch EC2 Instance (7 mins)

**Console:** EC2 → Launch Instance

1. **Name:** `Care4U-Hospital-Server`
2. **AMI:** Amazon Linux 2023 (Free Tier)
3. **Instance type:** t2.micro (Free Tier)
4. **Key pair:** Proceed without a key pair
5. **Network settings:**
   - Auto-assign public IP: Enable
   - Security group rules:
     - SSH (22) - My IP
     - HTTP (80) - Anywhere
     - Custom TCP (5000) - Anywhere
6. **Advanced details:**
   - IAM instance profile: `Care4U_EC2_Role`
7. **Launch instance**
8. **Copy the Public IPv4 address**

---

### Step 5: Deploy Application (10 mins)

#### 5.1 Connect to EC2

**Console:** EC2 → Instances → Select instance → Connect → EC2 Instance Connect → Connect

#### 5.2 Clone and Setup

Run these commands in the EC2 terminal:

```bash
# Clone the repository
git clone https://github.com/Pramodh92/Care_4_U-Hospitals-appointment-system.git

# Navigate to project
cd Care_4_U-Hospitals-appointment-system

# Run setup script
bash setup_ec2.sh
```

#### 5.3 Set SNS Topic ARN

```bash
# Set your SNS Topic ARN (from Step 3)
export SNS_TOPIC_ARN='arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:Care4U_Appointments'
```

#### 5.4 Start the Application

```bash
# Navigate to backend
cd backend

# Run the application
python3 app.py
```

**Expected output:**
```
🏥 Starting Care_4_U Hospitals Application...
============================================================
📋 Doctors table is empty. Auto-seeding doctor data...
============================================================
  ✓ Added: Dr. Sarah Johnson (Cardiology)
  ✓ Added: Dr. Michael Chen (Pediatrics)
  ✓ Added: Dr. Emily Davis (Dermatology)
  ✓ Added: Dr. Robert Martinez (Orthopedics)
  ✓ Added: Dr. Jennifer Lee (General Medicine)
============================================================
✅ Auto-seeding complete: 5/5 doctors added
============================================================

🚀 Starting Flask server on http://0.0.0.0:5000
```

---

## 🎉 Test Your Application

1. **Open browser:** `http://YOUR_EC2_PUBLIC_IP:5000`
2. **Sign up** with your details
3. **Login** with your credentials
4. **View doctors** - You should see all 5 doctors!
5. **Book appointment** - Select doctor, date, time
6. **Check email** - You should receive confirmation

---

## ✅ Success Checklist

- [ ] IAM role created and attached to EC2
- [ ] 3 DynamoDB tables created (empty)
- [ ] SNS topic created and email confirmed
- [ ] EC2 instance running
- [ ] Application cloned and setup complete
- [ ] Flask server running on port 5000
- [ ] 5 doctors auto-seeded into DynamoDB
- [ ] Can access application in browser
- [ ] Can sign up and login
- [ ] Can view all doctors
- [ ] Can book appointments
- [ ] Email notifications received

---

## 🔧 Quick Troubleshooting

**Can't access application?**
- Check EC2 security group allows port 5000
- Verify EC2 public IP is correct
- Ensure Flask is running: `ps aux | grep app.py`

**No doctors showing?**
- Check Flask startup logs for auto-seeding messages
- Verify DynamoDB table `Care4U_Doctors` has 5 items
- Check IAM role has DynamoDB permissions

**No email received?**
- Confirm SNS subscription is "Confirmed" status
- Check spam/junk folder
- Verify SNS_TOPIC_ARN is set correctly

---

## 📚 Next Steps

- Review [DEPLOYMENT.md](DEPLOYMENT.md) for detailed explanations
- Check [README.md](README.md) for API documentation
- Explore [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for architecture details

---

**Deployment Time:** ~30 minutes  
**Cost:** $0 (within AWS Free Tier)  
**Difficulty:** Beginner-friendly

🎓 Perfect for learning AWS services integration!
