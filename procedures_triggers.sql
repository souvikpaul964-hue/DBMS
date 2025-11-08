-- Stored Procedures, Triggers, Views, and Functions
-- REFINED VERSION: Removed triggers that duplicated Python-side logic.

-- =====================================================
-- DROP EXISTING OBJECTS (if they exist)
-- =====================================================

-- Drop Procedures
DROP PROCEDURE IF EXISTS GetRoomAvailabilityCount;
DROP PROCEDURE IF EXISTS CalculateBookingTotal;
DROP PROCEDURE IF EXISTS GetGuestBookingSummary;
DROP PROCEDURE IF EXISTS GetDailyRevenue;
DROP PROCEDURE IF EXISTS ProcessCheckIn;
DROP PROCEDURE IF EXISTS ProcessCheckOut;

-- Drop Triggers
DROP TRIGGER IF EXISTS before_booking_insert;
DROP TRIGGER IF EXISTS before_booking_delete;

-- Drop Views
DROP VIEW IF EXISTS vw_available_rooms;
DROP VIEW IF EXISTS vw_current_bookings;
DROP VIEW IF EXISTS vw_revenue_summary;
DROP VIEW IF EXISTS vw_guest_statistics;
DROP VIEW IF EXISTS vw_room_occupancy;

-- Drop Functions
DROP FUNCTION IF EXISTS CalculateNights;
DROP FUNCTION IF EXISTS GetRoomPrice;
DROP FUNCTION IF EXISTS IsRoomAvailable;

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

-- Procedure 1: Get Room Availability Count
DELIMITER //
CREATE PROCEDURE GetRoomAvailabilityCount(
    IN p_check_in DATE,
    IN p_check_out DATE,
    IN p_room_type VARCHAR(50)
)
BEGIN
    SELECT rt.type_name, COUNT(r.room_id) AS available_count
    FROM rooms r
    JOIN room_types rt ON r.type_id = rt.type_id
    WHERE r.status = 'available'
    AND (p_room_type IS NULL OR rt.type_name = p_room_type)
    AND r.room_id NOT IN (
        SELECT room_id FROM bookings
        WHERE booking_status IN ('confirmed', 'checked-in')
        AND check_in_date < p_check_out 
        AND check_out_date > p_check_in
    )
    GROUP BY rt.type_name;
END //
DELIMITER ;

-- Procedure 2: Calculate Booking Total
DELIMITER //
CREATE PROCEDURE CalculateBookingTotal(
    IN p_room_id INT,
    IN p_check_in DATE,
    IN p_check_out DATE,
    OUT p_total_amount DECIMAL(10,2),
    OUT p_num_nights INT
)
BEGIN
    DECLARE v_base_price DECIMAL(10,2);
    
    SET p_num_nights = DATEDIFF(p_check_out, p_check_in);
    
    SELECT base_price INTO v_base_price
    FROM room_types
    WHERE type_id = (SELECT type_id FROM rooms WHERE room_id = p_room_id);
    
    SET p_total_amount = v_base_price * p_num_nights;
END //
DELIMITER ;

-- Procedure 3: Get Guest Booking Summary
DELIMITER //
CREATE PROCEDURE GetGuestBookingSummary(IN p_guest_id INT)
BEGIN
    SELECT 
        COUNT(*) AS total_bookings,
        SUM(CASE WHEN booking_status = 'checked-out' THEN 1 ELSE 0 END) AS completed_bookings,
        SUM(CASE WHEN booking_status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_bookings,
        SUM(total_amount) AS total_spent,
        MIN(check_in_date) AS first_visit,
        MAX(check_out_date) AS last_visit
    FROM bookings
    WHERE guest_id = p_guest_id;
END //
DELIMITER ;

-- Procedure 4: Get Daily Revenue
DELIMITER //
CREATE PROCEDURE GetDailyRevenue(IN p_date DATE)
BEGIN
    SELECT 
        DATE(payment_date) AS date,
        COUNT(*) AS transactions,
        SUM(amount) AS total_revenue,
        AVG(amount) AS avg_transaction,
        SUM(CASE WHEN payment_method = 'cash' THEN amount ELSE 0 END) AS cash_revenue,
        SUM(CASE WHEN payment_method = 'credit_card' THEN amount ELSE 0 END) AS card_revenue,
        SUM(CASE WHEN payment_method = 'upi' THEN amount ELSE 0 END) AS upi_revenue
    FROM payments
    WHERE DATE(payment_date) = p_date
    AND payment_status = 'completed'
    GROUP BY DATE(payment_date);
END //
DELIMITER ;

-- Procedure 5: Check-in Process
DELIMITER //
CREATE PROCEDURE ProcessCheckIn(
    IN p_booking_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(200)
)
BEGIN
    DECLARE v_room_id INT;
    DECLARE v_booking_status VARCHAR(20);
    DECLARE v_check_in_date DATE;
    
    -- Get booking details
    SELECT room_id, booking_status, check_in_date
    INTO v_room_id, v_booking_status, v_check_in_date
    FROM bookings
    WHERE booking_id = p_booking_id;
    
    -- Validate booking
    IF v_booking_status IS NULL THEN
        SET p_success = FALSE;
        SET p_message = 'Booking not found';
    ELSEIF v_booking_status = 'checked-in' THEN
        SET p_success = FALSE;
        SET p_message = 'Guest already checked in';
    ELSEIF v_booking_status = 'cancelled' THEN
        SET p_success = FALSE;
        SET p_message = 'Booking is cancelled';
    ELSE
        -- Process check-in
        UPDATE bookings 
        SET booking_status = 'checked-in', actual_check_in = NOW()
        WHERE booking_id = p_booking_id;
        
        UPDATE rooms 
        SET status = 'occupied'
        WHERE room_id = v_room_id;
        
        SET p_success = TRUE;
        SET p_message = 'Check-in successful';
    END IF;
END //
DELIMITER ;

-- Procedure 6: Check-out Process with Payment Validation
DELIMITER //
CREATE PROCEDURE ProcessCheckOut(
    IN p_booking_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(200),
    OUT p_pending_amount DECIMAL(10,2)
)
BEGIN
    DECLARE v_room_id INT;
    DECLARE v_booking_status VARCHAR(20);
    DECLARE v_total_amount DECIMAL(10,2);
    DECLARE v_paid_amount DECIMAL(10,2);
    
    -- Get booking details
    SELECT room_id, booking_status, total_amount
    INTO v_room_id, v_booking_status, v_total_amount
    FROM bookings
    WHERE booking_id = p_booking_id;
    
    -- Calculate paid amount
    SELECT COALESCE(SUM(amount), 0) INTO v_paid_amount
    FROM payments
    WHERE booking_id = p_booking_id AND payment_status = 'completed';
    
    SET p_pending_amount = v_total_amount - v_paid_amount;
    
    -- Validate
    IF v_booking_status IS NULL THEN
        SET p_success = FALSE;
        SET p_message = 'Booking not found';
    ELSEIF v_booking_status != 'checked-in' THEN
        SET p_success = FALSE;
        SET p_message = 'Guest is not checked in';
    ELSEIF p_pending_amount > 0 THEN
        SET p_success = FALSE;
        SET p_message = CONCAT('Pending payment: ₹', p_pending_amount);
    ELSE
        -- Process check-out
        UPDATE bookings 
        SET booking_status = 'checked-out', actual_check_out = NOW()
        WHERE booking_id = p_booking_id;
        
        -- MODIFICATION: Set to 'maintenance' to match Python logic
        UPDATE rooms 
        SET status = 'maintenance', last_cleaned = NOW()
        WHERE room_id = v_room_id;
        
        SET p_success = TRUE;
        SET p_message = 'Check-out successful';
    END IF;
END //
DELIMITER ;

-- =====================================================
-- TRIGGERS (VALIDATION ONLY)
-- =====================================================

-- Trigger 1: Validate booking dates
DELIMITER //
CREATE TRIGGER before_booking_insert
BEFORE INSERT ON bookings
FOR EACH ROW
BEGIN
    IF NEW.check_in_date >= NEW.check_out_date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Check-out date must be after check-in date';
    END IF;
    
    IF NEW.check_in_date < CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Check-in date cannot be in the past';
    END IF;
END //
DELIMITER ;

-- Trigger 2: Prevent deletion of checked-in bookings
DELIMITER //
CREATE TRIGGER before_booking_delete
BEFORE DELETE ON bookings
FOR EACH ROW
BEGIN
    IF OLD.booking_status = 'checked-in' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete a checked-in booking';
    END IF;
END //
DELIMITER ;

-- =====================================================
-- VIEWS
-- =====================================================

-- View 1: Available Rooms Summary
CREATE OR REPLACE VIEW vw_available_rooms AS
SELECT 
    r.room_id,
    r.room_number,
    rt.type_name,
    rt.base_price,
    rt.capacity,
    r.floor,
    r.status
FROM rooms r
JOIN room_types rt ON r.type_id = rt.type_id
WHERE r.status = 'available';

-- View 2: Current Bookings
CREATE OR REPLACE VIEW vw_current_bookings AS
SELECT 
    b.booking_id,
    b.check_in_date,
    b.check_out_date,
    b.booking_status,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.phone,
    r.room_number,
    rt.type_name,
    b.total_amount
FROM bookings b
JOIN guests g ON b.guest_id = g.guest_id
JOIN rooms r ON b.room_id = r.room_id
JOIN room_types rt ON r.type_id = rt.type_id
WHERE b.booking_status IN ('confirmed', 'checked-in');

-- View 3: Revenue Summary
CREATE OR REPLACE VIEW vw_revenue_summary AS
SELECT 
    DATE(payment_date) AS date,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    payment_method,
    payment_status
FROM payments
GROUP BY DATE(payment_date), payment_method, payment_status;

-- View 4: Guest Statistics
CREATE OR REPLACE VIEW vw_guest_statistics AS
SELECT 
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    g.email,
    g.phone,
    COUNT(b.booking_id) AS total_bookings,
    SUM(b.total_amount) AS total_spent,
    MAX(b.check_out_date) AS last_visit
FROM guests g
LEFT JOIN bookings b ON g.guest_id = b.guest_id
GROUP BY g.guest_id, g.first_name, g.last_name, g.email, g.phone;

-- View 5: Room Occupancy Status
CREATE OR REPLACE VIEW vw_room_occupancy AS
SELECT 
    rt.type_name,
    COUNT(r.room_id) AS total_rooms,
    SUM(CASE WHEN r.status = 'available' THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) AS occupied,
    SUM(CASE WHEN r.status = 'reserved' THEN 1 ELSE 0 END) AS reserved,
    SUM(CASE WHEN r.status = 'maintenance' THEN 1 ELSE 0 END) AS maintenance,
    ROUND((SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) / COUNT(r.room_id)) * 100, 2) AS occupancy_rate
FROM rooms r
JOIN room_types rt ON r.type_id = rt.type_id
GROUP BY rt.type_name;

-- =====================================================
-- FUNCTIONS
-- =====================================================

-- Function 1: Calculate nights between dates
DELIMITER //
CREATE FUNCTION CalculateNights(
    p_check_in DATE,
    p_check_out DATE
) RETURNS INT
DETERMINISTIC
BEGIN
    RETURN DATEDIFF(p_check_out, p_check_in);
END //
DELIMITER ;

-- Function 2: Get room base price
DELIMITER //
CREATE FUNCTION GetRoomPrice(p_room_id INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_price DECIMAL(10,2);
    
    SELECT base_price INTO v_price
    FROM room_types
    WHERE type_id = (SELECT type_id FROM rooms WHERE room_id = p_room_id);
    
    RETURN v_price;
END //
DELIMITER ;

-- Function 3: Check if room is available
DELIMITER //
CREATE FUNCTION IsRoomAvailable(
    p_room_id INT,
    p_check_in DATE,
    p_check_out DATE
) RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE v_count INT;
    
    SELECT COUNT(*) INTO v_count
    FROM bookings
    WHERE room_id = p_room_id
    AND booking_status IN ('confirmed', 'checked-in')
    AND check_in_date < p_check_out
    AND check_out_date > p_check_in;
    
    RETURN (v_count = 0);
END //
DELIMITER ;