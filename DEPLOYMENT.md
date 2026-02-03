# 🚀 AWS Deployment Guide - Care_4_U Hospitals

This guide provides **step-by-step instructions** for deploying the Care_4_U Hospitals appointment system on AWS using the AWS Console and EC2 terminal.

---

## 📋 Prerequisites

- AWS Account (Free Tier eligible)
- Web browser (Chrome, Firefox, Safari, or Edge)
- Email address for SNS notifications

---

## 🔐 Step 1: Create IAM Role for EC2

### 1.1 Navigate to IAM Console

1. Log in to AWS Console
2. Search for **IAM** in the search bar
3. Click on **IAM** service

### 1.2 Create Custom Policies

#### Create DynamoDB Policy

1. In IAM Console, click **Policies** → **Create policy**
2. Click **JSON** tab
3. Paste the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Scan",
        "dynamodb:Query",
        "dynamodb:UpdateItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:*:*:table/Care4U_Users",
        "arn:aws:dynamodb:*:*:table/Care4U_Doctors",
        "arn:aws:dynamodb:*:*:table/Care4U_Appointments"
      ]
    }
  ]
}
```

4. Click **Next: Tags** → **Next: Review**
5. **Policy name:** `Care4U_DynamoDB_Policy`
6. **Description:** `Allows EC2 to access Care4U DynamoDB tables`
7. Click **Create policy**

#### Create SNS Policy

1. Click **Policies** → **Create policy**
2. Click **JSON** tab
3. Paste the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:*:*:Care4U_Appointments"
    }
  ]
}
```

4. Click **Next: Tags** → **Next: Review**
5. **Policy name:** `Care4U_SNS_Policy`
6. **Description:** `Allows EC2 to publish SNS notifications`
7. Click **Create policy**

### 1.3 Create IAM Role

1. In IAM Console, click **Roles** → **Create role**
2. **Trusted entity type:** AWS service
3. **Use case:** EC2
4. Click **Next**
5. Search and select:
   - `Care4U_DynamoDB_Policy`
   - `Care4U_SNS_Policy`
6. Click **Next**
7. **Role name:** `Care4U_EC2_Role`
8. **Description:** `IAM role for Care4U EC2 instance`
9. Click **Create role**

✅ **IAM Role Created Successfully!**

---

## 🗄️ Step 2: Create DynamoDB Tables

### 2.1 Navigate to DynamoDB Console

1. Search for **DynamoDB** in AWS Console
2. Click on **DynamoDB** service

### 2.2 Create Users Table

1. Click **Create table**
2. **Table name:** `Care4U_Users`
3. **Partition key:** `user_id` (String)
4. **Table settings:** Default settings
5. Click **Create table**
6. Wait for table status to become **Active**

### 2.3 Create Doctors Table

1. Click **Create table**
2. **Table name:** `Care4U_Doctors`
3. **Partition key:** `doctor_id` (String)
4. **Table settings:** Default settings
5. Click **Create table**
6. Wait for table status to become **Active**

### 2.4 Create Appointments Table

1. Click **Create table**
2. **Table name:** `Care4U_Appointments`
3. **Partition key:** `appointment_id` (String)
4. **Table settings:** Default settings
5. Click **Create table**
6. Wait for table status to become **Active**

> [!IMPORTANT]
> **No Manual Data Entry Required!**
> 
> The `Care4U_Doctors` table should be left **empty**. Doctor data will be automatically populated when you run the Flask application for the first time. The app will detect the empty table and auto-seed 5 doctors with their specializations and available time slots.

✅ **DynamoDB Tables Created!**

---

## 📧 Step 3: Create SNS Topic

### 3.1 Navigate to SNS Console

1. Search for **SNS** in AWS Console
2. Click on **Simple Notification Service**

### 3.2 Create Topic

1. Click **Topics** → **Create topic**
2. **Type:** Standard
3. **Name:** `Care4U_Appointments`
4. **Display name:** `Care4U Hospitals`
5. Click **Create topic**
6. **Copy the Topic ARN** (you'll need this later)

### 3.3 Create Email Subscription

1. In the topic details page, click **Create subscription**
2. **Protocol:** Email
3. **Endpoint:** Enter your email address
4. Click **Create subscription**
5. **Check your email** and click the confirmation link
6. Return to SNS Console and verify subscription status is **Confirmed**

✅ **SNS Topic Created and Email Confirmed!**

---

## 🖥️ Step 4: Launch EC2 Instance

### 4.1 Navigate to EC2 Console

1. Search for **EC2** in AWS Console
2. Click on **EC2** service

### 4.2 Launch Instance

1. Click **Launch Instance**
2. **Name:** `Care4U-Hospital-Server`

### 4.3 Choose AMI

1. **Amazon Machine Image:** Amazon Linux 2023 AMI (Free Tier eligible)

### 4.4 Choose Instance Type

1. **Instance type:** t2.micro (Free Tier eligible)

### 4.5 Key Pair

**Select:** "Proceed without a key pair" (we'll use EC2 Instance Connect from the browser)


### 4.6 Configure Network Settings

1. Click **Edit** in Network settings
2. **Auto-assign public IP:** Enable
3. **Firewall (security groups):** Create security group
4. **Security group name:** `care4u-sg`
5. **Description:** `Security group for Care4U Hospital`

Add the following rules:

| Type | Protocol | Port Range | Source |
|------|----------|------------|--------|
| SSH | TCP | 22 | My IP |
| HTTP | TCP | 80 | Anywhere (0.0.0.0/0) |
| Custom TCP | TCP | 5000 | Anywhere (0.0.0.0/0) |

### 4.7 Attach IAM Role

1. Scroll to **Advanced details**
2. **IAM instance profile:** Select `Care4U_EC2_Role`

### 4.8 Launch Instance

1. Click **Launch instance**
2. Wait for instance state to become **Running**
3. **Copy the Public IPv4 address**

✅ **EC2 Instance Launched!**

---

## 📦 Step 5: Deploy Backend Application

### 5.1 Connect to EC2 Instance via AWS Console

1. Go to **EC2 Console** → **Instances**
2. Select your instance: `Care4U-Hospital-Server`
3. Click **Connect** button (top right)
4. Select **EC2 Instance Connect** tab
5. **Username:** `ec2-user` (default)
6. Click **Connect** button
7. A new browser tab will open with a terminal

✅ **Connected to EC2 Instance!**

### 5.2 Install Required Software

Copy and paste these commands in the EC2 terminal:

```bash
# Update system packages
sudo yum update -y

# Install Python 3 and pip
sudo yum install python3-pip -y

# Install Git
sudo yum install git -y

# Verify installations
python3 --version
pip3 --version
git --version
```

### 5.3 Clone the Project from GitHub

```bash
# Clone the Care_4_U Hospitals repository
git clone https://github.com/Pramodh92/Care_4_U-Hospitals-appointment-system.git

# Navigate to project directory
cd Care_4_U-Hospitals-appointment-system
```

### 5.4 Run Setup Script

```bash
# Run the automated setup script
bash setup_ec2.sh
```

This script will:
- Update system packages
- Install Python 3 and pip
- Install all required Python dependencies (Flask, boto3, etc.)
- Verify installations

### 5.5 Configure SNS Topic ARN

```bash
# Set SNS Topic ARN as environment variable (replace with your actual ARN from Step 3.2)
export SNS_TOPIC_ARN='arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:Care4U_Appointments'

# Add to .bashrc to persist across sessions (optional)
echo "export SNS_TOPIC_ARN='arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:Care4U_Appointments'" >> ~/.bashrc
```

### 5.6 Run Flask Backend Application

```bash
# Navigate to backend directory
cd backend

# Run Flask application
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
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://YOUR_PRIVATE_IP:5000
```

> [!NOTE]
> **Auto-Seeding Feature**
> 
> The application automatically checks if the `Care4U_Doctors` table is empty on startup. If empty, it will automatically populate the table with 5 doctors from the `local_data/doctors.json` file. This eliminates the need for manual data entry!

**To run in background:**
```bash
nohup python3 app.py > app.log 2>&1 &

# Check if running
ps aux | grep app.py

# View logs
tail -f app.log
# Press Ctrl+C to exit log view
```

✅ **Backend Deployed and Running!**

---

## 🌐 Step 6: Deploy Frontend Application

### 6.1 Update Frontend API Configuration

```bash
# Navigate to frontend directory
cd ~/Care_4_U-Hospitals-appointment-system/frontend

# Edit script.js to update API URL
nano script.js

# Find this line (around line 2):
# const API_BASE_URL = 'http://localhost:5000';

# Replace with your EC2 public IP:
# const API_BASE_URL = 'http://YOUR_EC2_PUBLIC_IP:5000';

# Press Ctrl+X, then Y, then Enter to save
```

### 6.2 Serve Frontend with Python HTTP Server

```bash
# Make sure you're in the frontend directory
cd ~/Care_4_U-Hospitals-appointment-system/frontend

# Run HTTP server on port 80 (requires sudo)
sudo python3 -m http.server 80 &
```

**Alternative: Use port 8000 (no sudo required)**
```bash
python3 -m http.server 8000 &
# Access via: http://YOUR_EC2_PUBLIC_IP:8000
```

### 6.3 Verify Both Services are Running

```bash
# Check running processes
ps aux | grep -E "app.py|http.server"

# You should see both Flask (port 5000) and HTTP server (port 80 or 8000)
```

✅ **Frontend Deployed!**

---

## 🧪 Step 7: Test the Application

### 7.1 Access the Application

Open your browser and navigate to:
```
http://YOUR_EC2_PUBLIC_IP
```

or if using port 8000:
```
http://YOUR_EC2_PUBLIC_IP:8000
```

### 7.2 Test User Flow

1. **Sign Up**
   - Click "Sign up here"
   - Fill in: Name, Email, Phone, Password
   - Click "Sign Up"
   - Should redirect to login page

2. **Login**
   - Enter email and password
   - Click "Login"
   - Should redirect to dashboard

3. **View Doctors**
   - Dashboard should display all 5 doctors
   - Verify names and specializations

4. **Book Appointment**
   - Click "Book Appointment"
   - Select a doctor
   - Choose date (today or future)
   - Select time slot
   - Click "Book Appointment"
   - Should see confirmation modal

5. **Check Email**
   - Check your email inbox
   - Should receive appointment confirmation
   - Verify all details are correct

### 7.3 Verify in AWS Console

#### Check DynamoDB:
1. Go to DynamoDB Console
2. Check **Care4U_Users** table → Should have your user
3. Check **Care4U_Appointments** table → Should have your appointment

#### Check SNS:
1. Go to SNS Console
2. Click on **Care4U_Appointments** topic
3. Click **Publish message** to test manually

✅ **Application Fully Functional!**

---

## 🔧 Common Issues & Fixes

### Issue 1: Cannot Connect via EC2 Instance Connect

**Problem:** EC2 Instance Connect fails to open terminal

**Solution:**
- Verify EC2 instance is in **Running** state
- Check that instance is using Amazon Linux 2023 AMI
- Ensure security group allows outbound internet access
- Try refreshing the AWS Console page
- Use a different browser (Chrome recommended)

### Issue 2: Backend Not Accessible

**Problem:** Cannot access `http://YOUR_IP:5000`

**Solution:**
```bash
# Check if Flask is running
ps aux | grep app.py

# Check logs
tail -f ~/care4u-app/backend/app.log

# Restart Flask
pkill -f app.py
cd ~/care4u-app/backend
nohup python3 app.py > app.log 2>&1 &
```

### Issue 3: DynamoDB Access Denied

**Problem:** Error accessing DynamoDB tables

**Solution:**
- Verify IAM role is attached to EC2 instance
- Check IAM policies are correct
- Ensure table names match exactly
- Verify region in `app.py` matches your DynamoDB region

### Issue 4: SNS Notification Not Received

**Problem:** No email after booking

**Solution:**
- Verify email subscription is confirmed in SNS Console
- Check spam/junk folder
- Verify SNS Topic ARN in `app.py` is correct
- Check EC2 has SNS publish permission

### Issue 5: Frontend Shows "Unable to Connect"

**Problem:** API calls failing

**Solution:**
- Verify `API_BASE_URL` in `script.js` is correct
- Check Flask backend is running
- Verify security group allows port 5000
- Check browser console for CORS errors

### Issue 6: Double Booking Not Prevented

**Problem:** Same slot can be booked twice

**Solution:**
- Verify appointment booking logic in `app.py`
- Check DynamoDB scan is working correctly
- Test with different time slots

---

## 🛑 Stopping the Application

```bash
# Stop Flask backend
pkill -f app.py

# Stop frontend server
sudo pkill -f "http.server 80"
# or
pkill -f "http.server 8000"
```

---

## 💰 Cost Management

### Free Tier Limits:
- **EC2:** 750 hours/month (t2.micro)
- **DynamoDB:** 25 GB storage, 25 read/write capacity units
- **SNS:** 1,000 email notifications/month

### To Avoid Charges:
1. **Stop EC2 instance** when not in use (doesn't delete data)
2. **Terminate EC2 instance** when done with project
3. **Delete DynamoDB tables** if no longer needed
4. **Delete SNS topic** if no longer needed

---

## 📝 Next Steps

1. **Add HTTPS:** Use AWS Certificate Manager + Load Balancer
2. **Custom Domain:** Use Route 53 for DNS
3. **Database Backup:** Enable DynamoDB point-in-time recovery
4. **Monitoring:** Set up CloudWatch alarms
5. **Auto Scaling:** Configure Auto Scaling Group for high availability

---

## 🎉 Congratulations!

You have successfully deployed the Care_4_U Hospitals appointment system on AWS!

**What you've learned:**
- ✅ IAM roles and policies
- ✅ DynamoDB table creation and data seeding
- ✅ SNS topic and email subscriptions
- ✅ EC2 instance configuration
- ✅ Flask application deployment
- ✅ Frontend hosting
- ✅ End-to-end testing

This project is now **resume-ready** and **interview-explainable**! 🚀
