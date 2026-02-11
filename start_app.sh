#!/bin/bash

# Start Backend
echo "Starting Backend..."
cd backend
source venv/bin/activate
pm2 start "python main.py" --name "backend"
deactivate
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
pm2 start "npm start" --name "frontend"
cd ..

echo "Application started!"
echo "Backend running on port 8000"
echo "Frontend running on port 3000"
echo ""
echo "To check status: pm2 status"
echo "To view logs: pm2 logs"
echo ""
echo "To expose to the internet (if you have ngrok account):"
echo "ngrok http 3000"
