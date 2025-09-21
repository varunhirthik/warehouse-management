#!/bin/bash

echo "🚀 Starting Cafe Warehouse Management System..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if database exists, create if not
if [ ! -f "warehouse.db" ]; then
    echo "Setting up database..."
    python database.py
fi

# Start the application
echo
echo "✅ Starting the application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo
python app.py
