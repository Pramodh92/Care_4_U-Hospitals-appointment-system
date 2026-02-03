# DynamoDB Doctor Data Import Guide

This guide provides **three methods** to populate the `Care4U_Doctors` DynamoDB table with initial doctor data, eliminating the need for manual console entry.

---

## 📋 Available Doctors Data

The following 5 doctors will be imported:

| Doctor ID | Name | Specialization | Available Slots |
|-----------|------|----------------|-----------------|
| doc-001 | Dr. Sarah Johnson | Cardiology | 09:00, 10:00, 11:00, 14:00, 15:00 |
| doc-002 | Dr. Michael Chen | Pediatrics | 09:00, 10:00, 11:00, 14:00, 15:00, 16:00 |
| doc-003 | Dr. Emily Davis | Dermatology | 10:00, 11:00, 14:00, 15:00, 16:00 |
| doc-004 | Dr. Robert Martinez | Orthopedics | 09:00, 10:00, 12:00, 14:00, 15:00 |
| doc-005 | Dr. Jennifer Lee | General Medicine | 09:00, 10:00, 11:00, 12:00, 14:00, 15:00, 16:00, 17:00 |

---

## 🚀 Method 1: Python Script (Recommended)

### Prerequisites
- Python 3.9+ installed
- AWS credentials configured (IAM role on EC2 or AWS CLI configured locally)
- `boto3` library installed

### Steps

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Run the seeding script:**
   ```bash
   python seed_doctors.py
   ```

3. **Expected output:**
   ```
   ============================================================
   Care_4_U Hospitals - Doctor Data Seeding Script
   ============================================================
   Region: us-east-1
   Table: Care4U_Doctors
   ============================================================
   Starting to seed 5 doctors into Care4U_Doctors...
   ✓ Added: Dr. Sarah Johnson (Cardiology)
   ✓ Added: Dr. Michael Chen (Pediatrics)
   ✓ Added: Dr. Emily Davis (Dermatology)
   ✓ Added: Dr. Robert Martinez (Orthopedics)
   ✓ Added: Dr. Jennifer Lee (General Medicine)

   ============================================================
   Seeding complete: 5/5 doctors added successfully
   ============================================================

   Total doctors in table: 5

   ✓ All doctors seeded successfully!
   ```

### Advantages
- ✅ Automated and fast
- ✅ Error handling included
- ✅ Verification built-in
- ✅ Can be run from EC2 instance or locally

---

## 🖥️ Method 2: AWS CLI Batch Write

### Prerequisites
- AWS CLI installed and configured
- Appropriate IAM permissions for DynamoDB

### Steps

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Run batch write command:**
   ```bash
   aws dynamodb batch-write-item --request-items file://doctors_dynamodb_format.json --region us-east-1
   ```

3. **Verify the import:**
   ```bash
   aws dynamodb scan --table-name Care4U_Doctors --region us-east-1
   ```

### Advantages
- ✅ No Python script needed
- ✅ Single command execution
- ✅ Works from any terminal with AWS CLI

---

## 🌐 Method 3: AWS Console Import (Manual but Visual)

### Steps

1. **Open DynamoDB Console:**
   - Navigate to: https://console.aws.amazon.com/dynamodb/
   - Select region: **us-east-1**

2. **Select the table:**
   - Click on `Care4U_Doctors` table

3. **Create items manually:**
   - Click **"Create item"** button
   - For each doctor, add the following attributes:

#### Doctor 1: Dr. Sarah Johnson
```json
{
  "doctor_id": "doc-001",
  "name": "Sarah Johnson",
  "specialization": "Cardiology",
  "available_slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
}
```

#### Doctor 2: Dr. Michael Chen
```json
{
  "doctor_id": "doc-002",
  "name": "Michael Chen",
  "specialization": "Pediatrics",
  "available_slots": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
}
```

#### Doctor 3: Dr. Emily Davis
```json
{
  "doctor_id": "doc-003",
  "name": "Emily Davis",
  "specialization": "Dermatology",
  "available_slots": ["10:00", "11:00", "14:00", "15:00", "16:00"]
}
```

#### Doctor 4: Dr. Robert Martinez
```json
{
  "doctor_id": "doc-004",
  "name": "Robert Martinez",
  "specialization": "Orthopedics",
  "available_slots": ["09:00", "10:00", "12:00", "14:00", "15:00"]
}
```

#### Doctor 5: Dr. Jennifer Lee
```json
{
  "doctor_id": "doc-005",
  "name": "Jennifer Lee",
  "specialization": "General Medicine",
  "available_slots": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]
}
```

---

## ✅ Verification

After using any method, verify the data was imported correctly:

### Using Python:
```python
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Care4U_Doctors')
response = table.scan()
print(f"Total doctors: {response['Count']}")
for doctor in response['Items']:
    print(f"- Dr. {doctor['name']} ({doctor['specialization']})")
```

### Using AWS CLI:
```bash
aws dynamodb scan --table-name Care4U_Doctors --region us-east-1 --query 'Count'
```

### Using AWS Console:
1. Go to DynamoDB Console
2. Select `Care4U_Doctors` table
3. Click **"Explore table items"**
4. Verify 5 doctors are listed

---

## 🔧 Troubleshooting

### Error: "Table does not exist"
**Solution:** Create the `Care4U_Doctors` table first with partition key `doctor_id` (String)

### Error: "Access Denied"
**Solution:** Ensure your IAM role/user has `dynamodb:PutItem` and `dynamodb:BatchWriteItem` permissions

### Error: "Module 'boto3' not found"
**Solution:** Install boto3:
```bash
pip install boto3
```

### Error: "AWS credentials not configured"
**Solution:** 
- On EC2: Attach IAM role with DynamoDB permissions
- Locally: Run `aws configure` and enter credentials

---

## 📝 Notes

- All methods populate the same data from `backend/local_data/doctors.json`
- The Python script is recommended for deployment automation
- The AWS CLI method is best for one-time setup
- Available slots are in 24-hour format (HH:MM)
- Each doctor has unique time slots based on their schedule

---

## 🎯 Recommended Workflow

**For New AWS Account Setup:**
1. Create DynamoDB table `Care4U_Doctors` (partition key: `doctor_id`)
2. Run `python seed_doctors.py` from EC2 instance
3. Verify data using the verification commands above
4. Start your Flask application

**For Local Development:**
1. Configure AWS credentials locally
2. Run `python seed_doctors.py`
3. Test your application endpoints

---

**Created for Care_4_U Hospitals Appointment System**
