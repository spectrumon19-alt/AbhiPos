@echo off
REM start_pos_system.bat - Easy start script for POS System

echo ========================================
echo Point of Sale System
echo ========================================

echo Starting POS System...
echo Make sure PostgreSQL is running and the database is initialized.
echo.
echo The application will be available at http://localhost:5001
echo Press CTRL+C to stop the server
echo.

python app.py

echo.
echo POS System stopped.
pause