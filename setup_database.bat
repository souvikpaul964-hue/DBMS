@echo off
echo ========================================
echo HOTEL MANAGEMENT SYSTEM - DATABASE SETUP
echo ========================================
echo.
echo This script will:
echo 1. Create the hotel_management database
echo 2. Import the database schema (tables)
echo 3. Import sample data
echo 4. Import stored procedures and triggers
echo.
echo You will be asked for your MySQL root password 4 times.
echo.
pause

echo.
echo [Step 1/4] Creating database...
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hotel_management;"
if %errorlevel% neq 0 (
    echo ERROR: Failed to create database
    echo Make sure MySQL is installed and running
    pause
    exit /b 1
)
echo Database created successfully!

echo.
echo [Step 2/4] Importing schema (creating tables)...
mysql -u root -p hotel_management < database_schema.sql
if %errorlevel% neq 0 (
    echo ERROR: Failed to import schema
    pause
    exit /b 1
)
echo Schema imported successfully!

echo.
echo [Step 3/4] Importing sample data...
mysql -u root -p hotel_management < sample_data.sql
if %errorlevel% neq 0 (
    echo ERROR: Failed to import sample data
    pause
    exit /b 1
)
echo Sample data imported successfully!

echo.
echo [Step 4/4] Importing procedures and triggers...
mysql -u root -p hotel_management < procedures_triggers.sql
if %errorlevel% neq 0 (
    echo ERROR: Failed to import procedures
    pause
    exit /b 1
)
echo Procedures and triggers imported successfully!

echo.
echo ========================================
echo DATABASE SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Open hotel_management.py
echo 2. Change PASSWORD = "your_password" to your MySQL password
echo 3. Run: python hotel_management.py
echo.
pause
