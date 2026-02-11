#!/bin/bash

# Exit on error
set -e

echo "Updating system packages..."
sudo apt-get update
sudo apt-get install -y curl git python3 python3-pip python3-venv unzip

# Install Node.js (v20)
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 for process management
echo "Installing PM2..."
sudo npm install -g pm2

# Backend Setup
echo "Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Check if .env exists, if not copy example (user still needs to edit it)
if [ ! -f .env ]; then
    cp .env.example .env
    echo "WARNING: Created .env from example. Please update backend/.env with your API keys!"
fi
deactivate
cd ..

# Frontend Setup
echo "Setting up Frontend..."
cd frontend
npm install
npm run build
cd ..

# Install ngrok for public access (optional but recommended)
echo "Installing ngrok..."
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok

echo "Setup Complete!"
echo "To start the application, use the start_app.sh script (created next)."
