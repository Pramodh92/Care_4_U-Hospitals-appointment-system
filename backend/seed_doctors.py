#!/usr/bin/env python3
"""
DynamoDB Doctor Data Seeding Script
This script populates the Care4U_Doctors table with initial doctor data.
"""

import boto3
import json
import os
from botocore.exceptions import ClientError

# AWS Configuration
REGION = 'us-east-1'
TABLE_NAME = 'Care4U_Doctors'

def load_doctor_data():
    """Load doctor data from JSON file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'local_data', 'doctors.json')
    
    with open(json_path, 'r') as f:
        return json.load(f)

def seed_doctors():
    """Seed doctors data into DynamoDB table"""
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb', region_name=REGION)
        table = dynamodb.Table(TABLE_NAME)
        
        # Load doctor data
        doctors = load_doctor_data()
        
        print(f"Starting to seed {len(doctors)} doctors into {TABLE_NAME}...")
        
        # Insert each doctor
        success_count = 0
        for doctor in doctors:
            try:
                table.put_item(Item=doctor)
                print(f"✓ Added: Dr. {doctor['name']} ({doctor['specialization']})")
                success_count += 1
            except ClientError as e:
                print(f"✗ Failed to add Dr. {doctor['name']}: {e.response['Error']['Message']}")
        
        print(f"\n{'='*60}")
        print(f"Seeding complete: {success_count}/{len(doctors)} doctors added successfully")
        print(f"{'='*60}")
        
        # Verify by scanning the table
        response = table.scan()
        print(f"\nTotal doctors in table: {response['Count']}")
        
        return success_count == len(doctors)
        
    except ClientError as e:
        print(f"Error accessing DynamoDB: {e.response['Error']['Message']}")
        return False
    except FileNotFoundError:
        print("Error: doctors.json file not found in local_data directory")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

if __name__ == '__main__':
    print("="*60)
    print("Care_4_U Hospitals - Doctor Data Seeding Script")
    print("="*60)
    print(f"Region: {REGION}")
    print(f"Table: {TABLE_NAME}")
    print("="*60)
    
    success = seed_doctors()
    
    if success:
        print("\n✓ All doctors seeded successfully!")
        exit(0)
    else:
        print("\n✗ Seeding completed with errors")
        exit(1)
