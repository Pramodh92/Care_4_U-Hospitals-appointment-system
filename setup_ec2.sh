#!/bin/bash

# ============================================
# Care_4_U Hospitals - EC2 Setup Script
# ============================================
# This script sets up the EC2 instance after cloning the repository
# Run this script once after cloning: bash setup_ec2.sh

echo "============================================"
echo "🏥 Care_4_U Hospitals - EC2 Setup"
echo "============================================"
echo ""

# Update system packages
echo "📦 Updating system packages..."
sudo yum update -y

# Install Python 3 and pip
echo "🐍 Installing Python 3 and pip..."
sudo yum install python3-pip -y

# Install required Python packages
echo "📚 Installing Python dependencies..."
pip3 install flask flask-cors boto3 werkzeug

# Verify installations
echo ""
echo "✅ Verifying installations..."
python3 --version
pip3 --version

echo ""
echo "============================================"
echo "✅ Setup Complete!"
echo "============================================"
echo ""
echo "📝 Next Steps:"
echo "1. Set your SNS Topic ARN (if not using environment variable):"
echo "   export SNS_TOPIC_ARN='arn:aws:sns:REGION:ACCOUNT_ID:Care4U_Appointments'"
echo ""
echo "2. Run the application:"
echo "   cd backend"
echo "   python3 app.py"
echo ""
echo "3. Access the application:"
echo "   http://YOUR_EC2_PUBLIC_IP:5000"
echo ""
echo "============================================"
