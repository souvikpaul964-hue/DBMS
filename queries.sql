-- Useful Queries for Hotel Management System

-- 1. Check Available Rooms for a Date Range (LOGIC CORRECTED)
-- Set your desired dates here
SET @p_check_in = '2024-01-18';
SET @p_check_out = '2024-01-20';

SELECT r.room_id, r.room_number, rt.type_name, rt.base_price, r.floor
FROM rooms r
JOIN room_types rt ON r.type_id = rt.type_id
WHERE r.status = 'available'
AND r.room_id NOT IN (
    SELECT room_id FROM bookings
    WHERE booking_status IN ('confirmed', 'checked-in')
    -- This logic correctly finds any overlapping booking
    AND check_in_date < @p_check_out
    AND check_out_date > @p_check_in
);

-- 2. View All Current Check-ins
SELECT b.booking_id, g.first_name, g.last_name, g.phone, 
       r.room_number, rt.type_name, b.check_in_date, b.check_out_date
FROM bookings b
JOIN guests g ON b.guest_id = g.guest_id
JOIN rooms r ON b.room_id = r.room_id
JOIN room_types rt ON r.type_id = rt.type_id
WHERE b.booking_status = 'checked-in'
ORDER BY r.room_number;

-- 3. Total Revenue by Month
SELECT 
    DATE_FORMAT(payment_date, '%Y-%m') AS month,
    SUM(amount) AS total_revenue,
    COUNT(*) AS total_transactions
FROM payments
WHERE payment_status = 'completed'
GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
ORDER BY month DESC;

-- 4. Room Occupancy Report
SELECT 
    rt.type_name,
    COUNT(r.room_id) AS total_rooms,
    SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) AS occupied_rooms,
    SUM(CASE WHEN r.status = 'available' THEN 1 ELSE 0 END) AS available_rooms,
    ROUND((SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2) AS occupancy_rate
FROM rooms r
JOIN room_types rt ON r.type_id = rt.type_id
GROUP BY rt.type_name;

-- 5. Guest Booking History
SELECT 
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.email,
    COUNT(b.booking_id) AS total_bookings,
    SUM(b.total_amount) AS total_spent
FROM guests g
LEFT JOIN bookings b ON g.guest_id = b.guest_id
GROUP BY g.guest_id, g.first_name, g.last_name, g.email
ORDER BY total_bookings DESC;

-- 6. Upcoming Check-ins for Today
SELECT 
    b.booking_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.phone,
    r.room_number,
    rt.type_name,
    b.num_adults,
    b.num_children,
    b.special_requests
FROM bookings b
JOIN guests g ON b.guest_id = g.guest_id
JOIN rooms r ON b.room_id = r.room_id
JOIN room_types rt ON r.type_id = rt.type_id
WHERE b.check_in_date = CURDATE()
AND b.booking_status = 'confirmed'
ORDER BY r.room_number;

-- 7. Rooms Due for Check-out Today
SELECT 
    b.booking_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.phone,
    r.room_number,
    b.total_amount,
    COALESCE(SUM(p.amount), 0) AS paid_amount,
    (b.total_amount - COALESCE(SUM(p.amount), 0)) AS pending_amount
FROM bookings b
JOIN guests g ON b.guest_id = g.guest_id
JOIN rooms r ON b.room_id = r.room_id
LEFT JOIN payments p ON b.booking_id = p.booking_id AND p.payment_status = 'completed'
WHERE b.check_out_date = CURDATE()
AND b.booking_status = 'checked-in'
GROUP BY b.booking_id, g.first_name, g.last_name, g.phone, r.room_number, b.total_amount;

-- 8. Staff Details by Department
SELECT 
    d.department_name,
    COUNT(s.staff_id) AS total_staff,
    AVG(s.salary) AS avg_salary,
    SUM(s.salary) AS total_salary_expense
FROM departments d
LEFT JOIN staff s ON d.department_id = s.department_id AND s.status = 'active'
GROUP BY d.department_name
ORDER BY total_staff DESC;

-- 9. Rooms Needing Maintenance
SELECT 
    r.room_number,
    rt.type_name,
    r.floor,
    r.last_cleaned,
    DATEDIFF(NOW(), r.last_cleaned) AS days_since_cleaned
FROM rooms r
JOIN room_types rt ON r.type_id = rt.type_id
WHERE r.status = 'maintenance' OR DATEDIFF(NOW(), r.last_cleaned) > 7
ORDER BY r.floor, r.room_number;

-- 10. Most Popular Room Types
SELECT 
    rt.type_name,
    COUNT(b.booking_id) AS total_bookings,
    SUM(b.total_amount) AS total_revenue,
    AVG(b.total_amount) AS avg_booking_value
FROM room_types rt
JOIN rooms r ON rt.type_id = r.type_id
JOIN bookings b ON r.room_id = b.room_id
WHERE b.booking_status IN ('checked-in', 'checked-out')
GROUP BY rt.type_name
ORDER BY total_bookings DESC;

-- 11. Search Guest by Name or Phone
SELECT 
    guest_id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    email,
    phone,
    city,
    country
FROM guests
WHERE first_name LIKE '%Arjun%' 
   OR last_name LIKE '%Arjun%'
   OR phone LIKE '%9123456789%'
   OR email LIKE '%arjun%';

-- 12. Booking Summary for a Specific Guest
SELECT 
    b.booking_id,
    r.room_number,
    rt.type_name,
    b.check_in_date,
    b.check_out_date,
    b.booking_status,
    b.total_amount,
    COALESCE(SUM(p.amount), 0) AS paid_amount
FROM bookings b
JOIN rooms r ON b.room_id = r.room_id
JOIN room_types rt ON r.type_id = rt.type_id
LEFT JOIN payments p ON b.booking_id = p.booking_id AND p.payment_status = 'completed'
WHERE b.guest_id = 1
GROUP BY b.booking_id, r.room_number, rt.type_name, b.check_in_date, 
         b.check_out_date, b.booking_status, b.total_amount
ORDER BY b.check_in_date DESC;