# TESTING GUIDE - Hotel Management System

## Pre-requisites Checklist
- [ ] MySQL is running
- [ ] Database 'hotel_management' created
- [ ] database_schema.sql imported
- [ ] sample_data.sql imported
- [ ] Python packages installed (run setup.bat)
- [ ] Password updated in hotel_management.py

---

## How to Run

### Step 1: Open Command Prompt
```bash
cd "C:\Users\Souvik\Desktop\DBMS"
```

### Step 2: Start the Application
```bash
python hotel_management.py
```

You should see:
```
Successfully connected to the database

==============================================================
   HOTEL MANAGEMENT SYSTEM - PREMIUM EDITION
==============================================================
```

---

## Feature Testing Guide

### 🔰 BASIC FEATURES

#### Test 1: Search Existing Guest
```
Choice: 2
Search: Arjun
Expected: Shows Guest ID 1, Arjun Mehta's details
```

#### Test 2: View Available Rooms
```
Choice: 3
Check-in: 2024-02-01
Check-out: 2024-02-05
Expected: Lists available rooms with Room IDs and prices
```

#### Test 3: Add New Guest
```
Choice: 1
First Name: John
Last Name: Doe
Email: john.doe@email.com
Phone: 9999999999
(Fill other fields or press Enter for optional)
Expected: Shows "Guest added successfully! Guest ID: 7"
```

#### Test 4: View Current Check-ins
```
Choice: 7
Expected: Shows guest in Room 104 (from sample data)
```

#### Test 5: View Booking Details
```
Choice: 10
Booking ID: 1
Expected: Shows complete booking information
```

---

### ⭐ ADVANCED FEATURES (Unique!)

#### Test 6: Check Loyalty Status
```
Choice: 11
Guest ID: 1
Expected: Shows loyalty tier (Bronze/Silver/Gold/Platinum)
         Shows discount percentage and benefits
```

#### Test 7: AI Room Recommendations
```
Choice: 12
Guest ID: 1
Check-in: 2024-03-01
Check-out: 2024-03-05
Expected: Shows 5 recommended rooms based on guest history
         Shows recommendation score (100/80/60)
```

#### Test 8: Apply Special Offer
```
Choice: 13
Booking ID: 2
Offer Code: WEEKEND20
Expected: Shows 20% discount applied
         Original amount vs New amount
```

#### Test 9: Checkout Reminders
```
Choice: 14
Expected: Shows today's checkout list
         Shows pending payments if any
```

#### Test 10: Housekeeping Schedule
```
Choice: 15
Expected: Shows rooms to clean today
         Shows priority (High/Medium/Low)
```

#### Test 11: Add Feedback
```
Choice: 16
Booking ID: 4
Rating: 5
Comment: Excellent service!
Expected: Shows "Thank you for your feedback! Rating: ⭐⭐⭐⭐⭐"
```

---

### 📊 REPORTS & ANALYTICS

#### Test 12: Occupancy Report
```
Choice: 17
Expected: Shows room type-wise occupancy
         Shows percentages for each type
```

#### Test 13: Revenue Report
```
Choice: 18
Expected: Shows total revenue, transactions, average
```

#### Test 14: Advanced Analytics (Best Feature!)
```
Choice: 19
Expected: Shows comprehensive business metrics:
         - Monthly revenue
         - Occupancy rate
         - Top room type
         - Guest retention rate
         - Returning guests statistics
```

#### Test 15: Hotel Rating
```
Choice: 20
Expected: Shows average rating with stars
         Shows total number of reviews
```

---

### 💰 COMPLETE BOOKING WORKFLOW

#### Test 16: Create Full Booking
```
Step 1: Choice 3 - Check available rooms
        Dates: 2024-02-10 to 2024-02-15
        Note the Room ID

Step 2: Choice 4 - Create Booking
        Guest ID: 1
        Room ID: (from step 1)
        Check-in: 2024-02-10
        Check-out: 2024-02-15
        Adults: 2
        Children: 0
        Expected: Shows "Booking created! Booking ID: X"

Step 3: Choice 5 - Check-in
        Booking ID: (from step 2)
        Expected: "Check-in successful"

Step 4: Choice 9 - Add Payment
        Booking ID: (from step 2)
        Amount: (total amount shown)
        Method: credit_card
        Transaction ID: TEST123
        Expected: "Payment recorded successfully"

Step 5: Choice 6 - Check-out
        Booking ID: (from step 2)
        Expected: "Check-out successful"
```

---

## Sample Test Data

**Available Guest IDs:** 1, 2, 3, 4, 5, 6
**Available Room IDs:** 1-12
**Current Bookings:** 1, 2, 3, 4, 5, 6

**Special Offer Codes:**
- WEEKEND20 (20% off)
- FIRSTTIME (15% off)
- LOYALTY10 (10% off)
- EARLYBIRD (12% off)

---

## Expected Results Summary

### What Should Work:
✅ All 20 menu options
✅ Guest search by name/email/phone
✅ Room availability checking
✅ Dynamic pricing
✅ Loyalty tier calculation
✅ AI-based recommendations
✅ Special offers
✅ Feedback system
✅ Advanced analytics

### Unique Features to Highlight:
⭐ AI Room Recommendations (Choice 12)
⭐ Loyalty Program with 4 tiers (Choice 11)
⭐ Advanced Analytics Dashboard (Choice 19)
⭐ Special Offer System (Choice 13)
⭐ Smart Housekeeping Scheduler (Choice 15)
⭐ Guest Retention Analytics (Choice 19)

---

## Quick Demo Sequence

For a 5-minute demo, test in this order:
1. Choice 19 - Advanced Analytics (impressive!)
2. Choice 11 - Loyalty Status (Guest ID: 1)
3. Choice 12 - AI Recommendations (Guest ID: 1)
4. Choice 13 - Apply Offer (Booking 2, Code: WEEKEND20)
5. Choice 15 - Housekeeping Schedule
6. Choice 20 - Hotel Rating

---

## Troubleshooting

**Issue:** "Failed to connect to database"
**Fix:** Check MySQL is running, password is correct

**Issue:** "No guests found"
**Fix:** Make sure sample_data.sql was imported

**Issue:** "Booking not found"
**Fix:** Use existing booking IDs (1-6) from sample data

**Issue:** ModuleNotFoundError
**Fix:** Run: `pip install mysql-connector-python`

---

## Performance Check

The application should:
- ✅ Connect to database in < 2 seconds
- ✅ Show menu instantly
- ✅ Execute queries in < 1 second
- ✅ Handle invalid inputs gracefully
- ✅ Show clear error messages

---

**Ready to test!** Start with setup.bat, then run the application!
