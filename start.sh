#!/bin/bash

echo "Starting Flash Tans Application..."
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "IMPORTANT: Please edit .env file with your database credentials!"
fi

echo ""
echo "Starting application on 0.0.0.0:8000..."
echo "Access the application at: http://YOUR_FLOATING_IP:8000"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the application
python3 app.py
