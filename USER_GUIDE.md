# Hotel Management System - Complete User Guide

## How to Use Each Feature (with Examples)

---

## 🔰 BASIC OPERATIONS

### 1. Add New Guest

**When to use:** First time a guest comes to the hotel  
**What you need:** Guest's basic information

**Example:**
```
Enter your choice: 1

--- Add New Guest ---
First Name: John
Last Name: Doe
Email: john.doe@email.com
Phone: 9876543299
Address (optional): 123 Park Street
City (optional): Mumbai
Country (optional): India
ID Proof Type (optional): Aadhar
ID Proof Number (optional): XXXX-XXXX-5678

✅ Result: Guest added successfully! Guest ID: 7
```

**💡 Tip:** Save the Guest ID! You'll need it for creating bookings.

---

### 2. Search Guest

**When to use:** Find existing guests by name, email, or phone  
**What you need:** Any part of guest's name, email, or phone number

**Example 1 - Search by name:**
```
Enter your choice: 2

Enter name, email, or phone to search: Arjun

✅ Result:
Found 1 guest(s):

Guest ID: 1
Name: Arjun Mehta
Email: arjun.mehta@email.com
Phone: 9123456789
```

**Example 2 - Search by phone:**
```
Search: 9123456790

✅ Result: Shows Neha Gupta's details
```

---

### 3. View Available Rooms

**When to use:** Check which rooms are free for specific dates  
**What you need:** Check-in and check-out dates

**Example:**
```
Enter your choice: 3

Check-in date (YYYY-MM-DD): 2024-02-10
Check-out date (YYYY-MM-DD): 2024-02-15

✅ Result:
8 room(s) available:

Room ID: 1 | Room Number: 101 - Standard
Price: ₹2000/night
Capacity: 2 persons | Floor: 1

Room ID: 2 | Room Number: 102 - Standard
Price: ₹2000/night
Capacity: 2 persons | Floor: 1

... (more rooms)
```

**💡 Tip:** Note down the Room ID for booking!

---

### 4. Create Booking

**When to use:** Reserve a room for a guest  
**What you need:** Guest ID, Room ID, dates, number of guests

**Example:**
```
Enter your choice: 4

--- Create Booking ---
Guest ID: 1
Room ID: 2
Check-in date (YYYY-MM-DD): 2024-02-10
Check-out date (YYYY-MM-DD): 2024-02-15
Number of adults: 2
Number of children: 0
Special requests (optional): Late checkout if possible

✅ Result:
Booking created successfully! Booking ID: 9
Total Amount: ₹10000
```

**💡 Important:** Room status changes to 'reserved' automatically!

---

### 5. Check-in Guest

**When to use:** Guest arrives at the hotel  
**What you need:** Booking ID

**Example:**
```
Enter your choice: 5

Enter Booking ID for check-in: 9

✅ Result:
Check-in successful for booking 9
```

**What happens:**
- Room status changes to 'occupied'
- Actual check-in time is recorded
- Guest can now use the room

---

### 6. Check-out Guest

**When to use:** Guest is leaving the hotel  
**What you need:** Booking ID

**Example:**
```
Enter your choice: 6

Enter Booking ID for check-out: 9

✅ Result:
Check-out successful for booking 9. Room sent for cleaning.
```

**What happens:**
- Room status changes to 'maintenance' (for cleaning)
- Actual check-out time is recorded
- Room appears in housekeeping schedule

---

### 7. View Current Check-ins

**When to use:** See who's currently staying at the hotel  
**What you need:** Nothing

**Example:**
```
Enter your choice: 7

✅ Result:
1 guest(s) currently checked in:

Room 104 - Deluxe
Guest: Arjun Mehta
Phone: 9123456789
Check-out: 2024-01-18
```

---

### 8. Cancel Booking

**When to use:** Guest wants to cancel their reservation  
**What you need:** Booking ID

**Example:**
```
Enter your choice: 8

Enter Booking ID to cancel: 3

✅ Result:
Booking 3 cancelled successfully
```

**What happens:**
- Booking status changes to 'cancelled'
- Room becomes available again

---

### 9. Add Payment

**When to use:** Record payment from guest  
**What you need:** Booking ID, amount, payment method

**Example:**
```
Enter your choice: 9

--- Add Payment ---
Booking ID: 9
Amount: 5000
Payment Methods: cash, credit_card, debit_card, upi, net_banking
Payment Method: credit_card
Transaction ID (optional): TXN123456789

✅ Result:
Payment recorded successfully! Payment ID: 9
```

**💡 Tip:** You can accept partial payments. Guest can pay in installments!

---

### 10. View Booking Details

**When to use:** Get complete information about a booking  
**What you need:** Booking ID

**Example:**
```
Enter your choice: 10

Enter Booking ID: 1

✅ Result:
--- Booking Details ---
Booking ID: 1
Guest: Arjun Mehta
Phone: 9123456789
Room: 104 - Deluxe
Check-in: 2024-01-15
Check-out: 2024-01-18
Status: checked-in
Total Amount: ₹10500
```

---

## ⭐ ADVANCED FEATURES

### 11. Check Guest Loyalty Status

**When to use:** See guest's loyalty tier and benefits  
**What you need:** Guest ID

**Example:**
```
Enter your choice: 11

Enter Guest ID: 1

✅ Result:
==================================================
🌟 GUEST LOYALTY STATUS
==================================================
Tier: Silver
Discount: 10%
Total Bookings: 3
Total Spent: ₹32500.00
Benefits: Priority support, 10% discount
==================================================
```

**Loyalty Tiers:**
- **Bronze:** 0-1 bookings or < ₹20,000 (5% discount)
- **Silver:** 2-4 bookings or ₹20,000-49,999 (10% discount)
- **Gold:** 5-9 bookings or ₹50,000-99,999 (15% discount)
- **Platinum:** 10+ bookings or ₹100,000+ (20% discount)

---

### 12. Get Room Recommendations (AI)

**When to use:** Help guest choose best room based on their history  
**What you need:** Guest ID, check-in/out dates

**Example:**
```
Enter your choice: 12

Enter Guest ID: 1
Check-in date (YYYY-MM-DD): 2024-03-01
Check-out date (YYYY-MM-DD): 2024-03-05

✅ Result:
🤖 AI-POWERED ROOM RECOMMENDATIONS
Based on your previous stays, we recommend:

1. Room 204 - Suite
   Price: ₹6000/night
   Floor: 2 | Recommendation Score: 100/100

2. Room 301 - Suite
   Price: ₹6000/night
   Floor: 3 | Recommendation Score: 100/100

... (up to 5 recommendations)
```

**How AI works:**
- 100 points: Matches guest's previously booked room type
- 80 points: Higher floors (preferred by most guests)
- 60 points: Other available rooms

---

### 13. Apply Special Offer Code

**When to use:** Give discount to a booking  
**What you need:** Booking ID, Offer Code

**Example:**
```
Enter your choice: 13

Enter Booking ID: 2

Available Offers:
- WEEKEND20: 20% off on weekend bookings
- FIRSTTIME: 15% off for first-time guests
- LOYALTY10: 10% loyalty discount
- EARLYBIRD: 12% off for advance bookings

Enter Offer Code: WEEKEND20

✅ Result:
✅ 20% off on weekend bookings
Original Amount: ₹13500.00
Discount: ₹2700.00
New Amount: ₹10800.00
```

**💡 Tip:** Offer codes are case-insensitive!

---

### 14. Checkout Reminders for Today

**When to use:** See who needs to check out today  
**What you need:** Nothing (uses today's date)

**Example:**
```
Enter your choice: 14

✅ Result:
📅 CHECKOUT REMINDERS FOR TODAY (2024-01-18)
======================================================================

Room 104 - Arjun Mehta
Phone: 9123456789 | Email: arjun.mehta@email.com
Total: ₹10500.00 | Paid: ₹5000.00
⚠️ PENDING: ₹5500.00
```

**💡 Use this:** Check every morning to prepare for checkouts!

---

### 15. Housekeeping Schedule

**When to use:** See which rooms need cleaning  
**What you need:** Nothing

**Example:**
```
Enter your choice: 15

✅ Result:
🧹 HOUSEKEEPING SCHEDULE FOR TODAY
================================================================================
Room       Type            Floor    Status          Priority       
--------------------------------------------------------------------------------
303        Deluxe          3        maintenance     High Priority  
101        Standard        1        available       Medium Priority
102        Standard        1        available       Low Priority   
```

**Priority System:**
- **High Priority:** Maintenance status OR not cleaned in 3+ days
- **Medium Priority:** Not cleaned in 1-3 days
- **Low Priority:** Recently cleaned (< 1 day)

---

### 16. Add Guest Feedback

**When to use:** Guest wants to rate their stay  
**What you need:** Booking ID, Rating (1-5), Comment (optional)

**Example:**
```
Enter your choice: 16

Enter Booking ID: 4
Rating (1-5 stars): 5
Comment (optional): Excellent service and very clean rooms!

✅ Result:
✅ Thank you for your feedback! Rating: ⭐⭐⭐⭐⭐
```

---

## 📊 REPORTS & ANALYTICS

### 17. Occupancy Report

**When to use:** Check how many rooms are occupied by type  
**What you need:** Nothing

**Example:**
```
Enter your choice: 17

✅ Result:
--- Room Occupancy Report ---

Standard:
  Total Rooms: 4
  Occupied: 0
  Available: 3
  In Maintenance: 1
  Occupancy Rate: 0.00%

Deluxe:
  Total Rooms: 4
  Occupied: 1
  Available: 2
  In Maintenance: 1
  Occupancy Rate: 25.00%

Suite:
  Total Rooms: 2
  Occupied: 0
  Available: 2
  In Maintenance: 0
  Occupancy Rate: 0.00%

... (more room types)
```

---

### 18. Revenue Report

**When to use:** See total revenue and transactions  
**What you need:** Nothing (shows all-time data)

**Example:**
```
Enter your choice: 18

✅ Result:
--- Revenue Report (All Time) ---
Total Transactions: 8
Total Revenue: ₹70500.00
Average Transaction: ₹8812.50
```

---

### 19. Advanced Business Analytics

**When to use:** Get comprehensive business insights  
**What you need:** Nothing

**Example:**
```
Enter your choice: 19

✅ Result:
======================================================================
📊 ADVANCED BUSINESS ANALYTICS
======================================================================

💰 REVENUE METRICS:
   Monthly Revenue: ₹18000.00
   Transactions: 2
   Average Transaction: ₹9000.00

🏨 OCCUPANCY METRICS:
   Occupancy Rate: 8.33%
   Occupied Rooms: 1/12

🎯 PERFORMANCE METRICS:
   Top Room Type: Deluxe
   Top Room Revenue: ₹28500.00
   Guest Retention: 33.33%
   Returning Guests: 2/6
======================================================================
```

**What each metric means:**
- **Monthly Revenue:** This month's payment total
- **Occupancy Rate:** % of rooms currently occupied
- **Guest Retention:** % of guests who returned for another stay
- **Top Room Type:** Room type that earned most revenue

---

### 20. Hotel Rating & Reviews

**When to use:** See overall guest satisfaction  
**What you need:** Nothing

**Example:**
```
Enter your choice: 20

✅ Result:
==================================================
⭐ HOTEL RATING & REVIEWS
==================================================
Average Rating: 4.5/5.0 ⭐⭐⭐⭐
Total Reviews: 4
==================================================
```

---

## 🎯 Quick Demo Scenarios

### Scenario 1: New Guest Books a Room (5 minutes)

1. **Option 1:** Add guest (John Doe) → Get Guest ID: 7
2. **Option 3:** View available rooms for Feb 10-15 → Note Room ID: 2
3. **Option 4:** Create booking (Guest 7, Room 2) → Get Booking ID: 9
4. **Option 5:** Check-in (Booking 9)
5. **Option 9:** Add payment ₹5000
6. **Option 10:** View booking details (Booking 9)

### Scenario 2: Demonstrate Advanced Features (3 minutes)

1. **Option 11:** Check loyalty status (Guest 1) → Shows Silver tier
2. **Option 12:** Get AI recommendations (Guest 1)
3. **Option 13:** Apply offer WEEKEND20 to Booking 2
4. **Option 19:** Show advanced analytics

### Scenario 3: Daily Hotel Operations (2 minutes)

1. **Option 7:** View current check-ins
2. **Option 14:** Checkout reminders for today
3. **Option 15:** Housekeeping schedule
4. **Option 17:** Occupancy report

---

## 💡 Pro Tips

1. **Always search guests first** (Option 2) before creating bookings
2. **Check room availability** (Option 3) before promising dates to guests
3. **Use loyalty status** (Option 11) to offer appropriate discounts
4. **Check housekeeping schedule** (Option 15) every morning
5. **Review analytics** (Option 19) weekly to track business performance
6. **Collect feedback** (Option 16) from all guests before checkout

---

## 🚨 Common Mistakes to Avoid

❌ **Don't:** Try to check-in without creating a booking first  
✅ **Do:** Create Booking → Then Check-in

❌ **Don't:** Forget to add payment before check-out  
✅ **Do:** Check-out reminder will warn you about pending payments

❌ **Don't:** Use invalid date format (like 10/02/2024)  
✅ **Do:** Always use YYYY-MM-DD format (2024-02-10)

❌ **Don't:** Cancel a checked-in booking  
✅ **Do:** Check-out first, then cancel if needed

---

## 🎓 For Your College Presentation

**Most Impressive Features to Show:**
1. ⭐ **Option 19** - Advanced Analytics (shows all KPIs)
2. ⭐ **Option 12** - AI Room Recommendations (shows intelligence)
3. ⭐ **Option 11** - Loyalty Program (shows business logic)
4. ⭐ **Option 15** - Housekeeping Schedule (shows automation)

**Good Flow for Demo:**
Start → Analytics (19) → Search Guest (2) → AI Recommendations (12) → 
Apply Offer (13) → Show Loyalty (11) → Housekeeping (15) → Exit (0)

---

**Need more help?** Check `TESTING_GUIDE.md` for detailed test scenarios!
