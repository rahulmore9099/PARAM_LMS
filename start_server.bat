@echo off
echo ========================================
echo Smart LMS - Starting Development Server
echo ========================================
echo.
echo Server will start at: http://127.0.0.1:8000/
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

python manage.py runserver

pause
