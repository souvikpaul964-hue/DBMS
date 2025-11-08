@echo off
echo ========================================
echo HOTEL MANAGEMENT SYSTEM - SETUP
echo ========================================
echo.

echo [1/4] Installing Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install packages
    pause
    exit /b 1
)
echo Python packages installed successfully!
echo.

echo [2/4] Checking MySQL connection...
echo Please make sure MySQL is running!
echo.

echo [3/4] Next steps:
echo 1. Open MySQL Workbench or MySQL Command Line
echo 2. Run: CREATE DATABASE hotel_management;
echo 3. Run: USE hotel_management;
echo 4. Import database_schema.sql
echo 5. Import sample_data.sql
echo.

echo [4/4] Configuration:
echo Open hotel_management.py and update:
echo - PASSWORD = "your_mysql_password"
echo.

echo ========================================
echo Setup completed!
echo Run: python hotel_management.py
echo ========================================
pause
