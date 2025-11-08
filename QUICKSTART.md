# QUICK START GUIDE

## Installation Steps

### 1. Install Python Packages
Open Command Prompt in this folder and run:
```bash
pip install -r requirements.txt
```

OR double-click: **setup.bat**

### 2. Install MySQL (if not installed)
- Download from: https://dev.mysql.com/downloads/mysql/
- Install and remember your root password

### 3. Create Database
Open MySQL Command Line or MySQL Workbench and run:
```sql
CREATE DATABASE hotel_management;
USE hotel_management;
SOURCE database_schema.sql;
SOURCE sample_data.sql;
```

**Note:** The database schema now includes a `feedback` table used by the application. Importing `database_schema.sql` (which defines `feedback`) before `sample_data.sql` is required — if you previously let the app create the table at runtime, re-run `SOURCE database_schema.sql` to ensure `feedback` exists before importing `sample_data.sql`.

### 4. Configure Application
Open `hotel_management.py` and change:
```python
PASSWORD = "your_mysql_password"  # Line 383
```

### 5. Run Application
```bash
python hotel_management.py
```

---

## Required Software

✅ **Python 3.7+** - [Download](https://www.python.org/downloads/)
✅ **MySQL Server 5.7+** - [Download](https://dev.mysql.com/downloads/mysql/)
✅ **mysql-connector-python** - Auto-installed via requirements.txt

---

## Testing the Installation

After setup, try:
1. Option 2: Search Guest (search "Arjun")
2. Option 7: View Current Check-ins
3. Option 11: Guest Loyalty Status (Guest ID: 1)
4. Option 19: Advanced Analytics

---

## Troubleshooting

**Problem:** `pip: command not found`
**Solution:** Python not in PATH. Reinstall Python with "Add to PATH" checked

**Problem:** `Access denied for user 'root'`
**Solution:** Check your MySQL password in hotel_management.py

**Problem:** `No module named 'mysql'`
**Solution:** Run: `pip install mysql-connector-python`

**Problem:** `Unknown database 'hotel_management'`
**Solution:** Create database first using MySQL

---

## Quick Commands

```bash
# Install packages
pip install -r requirements.txt

# Run application
python hotel_management.py

# Check Python version
python --version

# Check pip
pip --version
```

---

**Need Help?** Check README.md for detailed documentation
