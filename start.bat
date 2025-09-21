@echo off
echo 🚀 Starting Cafe Warehouse Management System...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Check if database exists, create if not
if not exist "warehouse.db" (
    echo Setting up database...
    python database.py
)

REM Start the application
echo.
echo ✅ Starting the application...
echo 📱 Open your browser and go to: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.
python app.py

pause
