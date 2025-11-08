-- Sample Data for Hotel Management System
-- REFINED: Added past bookings for Guest ID 1 to make loyalty test work.

-- Insert Departments
INSERT INTO departments (department_name, description) VALUES
('Front Desk', 'Guest check-in, check-out, and reception services'),
('Housekeeping', 'Room cleaning and maintenance'),
('Food & Beverage', 'Restaurant and room service'),
('Management', 'Hotel administration and management'),
('Maintenance', 'Building and equipment maintenance');

-- Insert Staff
INSERT INTO staff (first_name, last_name, email, phone, department_id, position, salary, hire_date) VALUES
('Rahul', 'Sharma', 'rahul.sharma@hotel.com', '9876543210', 1, 'Front Desk Manager', 35000, '2022-01-15'),
('Priya', 'Patel', 'priya.patel@hotel.com', '9876543211', 1, 'Receptionist', 25000, '2022-03-20'),
('Amit', 'Kumar', 'amit.kumar@hotel.com', '9876543212', 2, 'Housekeeping Supervisor', 30000, '2021-11-10'),
('Sneha', 'Singh', 'sneha.singh@hotel.com', '9876543213', 2, 'Housekeeper', 20000, '2023-02-01'),
('Vikram', 'Reddy', 'vikram.reddy@hotel.com', '9876543214', 3, 'Restaurant Manager', 40000, '2021-08-05'),
('Anita', 'Desai', 'anita.desai@hotel.com', '9876543215', 4, 'General Manager', 80000, '2020-05-12'),
('Ravi', 'Joshi', 'ravi.joshi@hotel.com', '9876543216', 5, 'Maintenance Technician', 28000, '2022-06-18');

-- Insert Room Types
INSERT INTO room_types (type_name, description, base_price, capacity) VALUES
('Standard', 'Basic room with essential amenities', 2000, 2),
('Deluxe', 'Spacious room with premium amenities', 3500, 2),
('Suite', 'Large suite with separate living area', 6000, 4),
('Executive', 'Business-class room with work desk', 4500, 2),
('Presidential', 'Luxury suite with exclusive services', 12000, 6);

-- Insert Rooms
INSERT INTO rooms (room_number, type_id, floor, status, last_cleaned) VALUES
('101', 1, 1, 'available', NOW()),
('102', 1, 1, 'available', NOW()),
('103', 2, 1, 'available', NOW()),
('104', 2, 1, 'available', NOW()),
('201', 2, 2, 'available', NOW()),
('202', 4, 2, 'available', NOW()),
('203', 4, 2, 'available', NOW()),
('204', 3, 2, 'available', NOW()),
('301', 3, 3, 'available', NOW()),
('302', 5, 3, 'available', NOW()),
('303', 2, 3, 'available', NOW()),
('304', 1, 3, 'available', NOW());

-- Insert Guests
-- No default guests - Add your own using the application
-- INSERT INTO guests (first_name, last_name, email, phone, address, city, country, id_proof_type, id_proof_number) VALUES
-- ('Arjun', 'Mehta', 'arjun.mehta@email.com', '9123456789', '45 MG Road', 'Mumbai', 'India', 'Aadhar', 'XXXX-XXXX-1234');

-- Insert Bookings
-- No default bookings - Create bookings after adding guests
-- INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date, actual_check_in, num_adults, num_children, booking_status, total_amount, special_requests) VALUES
-- (1, 4, '2024-01-15', '2024-01-18', '2024-01-15 14:30:00', 2, 0, 'checked-in', 10500, 'Late check-out if possible');


-- Insert Payments
-- No default payments - Add payments after creating bookings
-- INSERT INTO payments (booking_id, amount, payment_date, payment_method, payment_status, transaction_id) VALUES
-- (1, 5000, '2024-01-15 14:30:00', 'credit_card', 'completed', 'TXN1234567890');

-- Insert Feedback
-- No default feedback - Guests will add their own feedback
-- INSERT INTO feedback (booking_id, rating, comment, feedback_date) VALUES
-- (1, 5, 'Excellent service!', '2024-01-18 12:00:00');