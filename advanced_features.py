import mysql.connector
from datetime import datetime, timedelta
from typing import List, Dict

class AdvancedHotelFeatures:
    
    def __init__(self, connection):
        self.connection = connection
    
    def calculate_dynamic_price(self, room_id: int, check_in_date: str) -> float:
        """
        Calculates a dynamic room price based on base price,
        hotel occupancy, and weekend dates.
        """
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                
                # --- Get Base Price ---
                cursor.execute("""
                    SELECT rt.base_price FROM rooms r
                    JOIN room_types rt ON r.type_id = rt.type_id
                    WHERE r.room_id = %s
                """, (room_id,))
                
                result = cursor.fetchone()
                
                # --- MODIFICATION: Added None check ---
                if not result:
                    print(f"Error: Room ID {room_id} not found.")
                    return 0.0  # Return a default or error value
                    
                base_price = float(result['base_price'])
                
                # --- Get Occupancy ---
                cursor.execute("""
                    SELECT COUNT(*) as bookings FROM bookings
                    WHERE check_in_date = %s AND booking_status IN ('confirmed', 'checked-in')
                """, (check_in_date,))
                
                bookings = cursor.fetchone()['bookings']
            
            # --- Apply Pricing Logic ---
            if bookings > 8:
                price = base_price * 1.25
            elif bookings > 5:
                price = base_price * 1.15
            else:
                price = base_price * 0.90
            
            # --- Apply Weekend Surcharge ---
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
            if check_in.weekday() in [4, 5]:  # 4 is Friday, 5 is Saturday
                price *= 1.20
            
            return round(price, 2)

        except Exception as e:
            print(f"Error calculating dynamic price: {e}")
            return 0.0 # Return 0 on error

    
    def get_guest_loyalty_tier(self, guest_id: int) -> Dict:
        """
        Determines a guest's loyalty tier based on their booking history.
        """
        # --- MODIFICATION: Using 'with' statement ---
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_bookings,
                    SUM(total_amount) as total_spent,
                    MAX(check_out_date) as last_visit
                FROM bookings
                WHERE guest_id = %s AND booking_status = 'checked-out'
            """, (guest_id,))
            
            data = cursor.fetchone()
        
        # This original logic for handling 'None' (no bookings) is already perfect.
        if not data or data['total_bookings'] == 0:
            return {
                'tier': 'Bronze', 'discount': 0, 'benefits': 'Standard benefits',
                'bookings': 0, 'spent': 0
            }
        
        bookings = data['total_bookings']
        spent = float(data['total_spent'] or 0)
        
        if bookings >= 10 or spent >= 100000:
            tier, discount, benefits = 'Platinum', 20, 'Free room upgrade, Late checkout, 20% discount'
        elif bookings >= 5 or spent >= 50000:
            tier, discount, benefits = 'Gold', 15, 'Priority check-in, Late checkout, 15% discount'
        elif bookings >= 2 or spent >= 20000:
            tier, discount, benefits = 'Silver', 10, 'Priority support, 10% discount'
        else:
            tier, discount, benefits = 'Bronze', 5, 'Standard benefits, 5% discount'
            
        return {
            'tier': tier, 'discount': discount, 'benefits': benefits,
            'bookings': bookings, 'spent': spent
        }
    
    def recommend_rooms(self, guest_id: int, check_in: str, check_out: str) -> List[Dict]:
        """
        Recommends available rooms, prioritizing the guest's past preferences.
        """
        # --- MODIFICATION: Using 'with' statement ---
        with self.connection.cursor(dictionary=True) as cursor:
            
            # --- Find guest's favorite room type ---
            cursor.execute("""
                SELECT rt.type_name, COUNT(*) as preference_count
                FROM bookings b
                JOIN rooms r ON b.room_id = r.room_id
                JOIN room_types rt ON r.type_id = rt.type_id
                WHERE b.guest_id = %s AND b.booking_status = 'checked-out'
                GROUP BY rt.type_name
                ORDER BY preference_count DESC
                LIMIT 1
            """, (guest_id,))
            
            preference = cursor.fetchone()
            # This 'if preference else None' is perfect, no change needed.
            preferred_type = preference['type_name'] if preference else None
            
            # --- Find available rooms and score them ---
            cursor.execute("""
                SELECT 
                    r.room_id, r.room_number, rt.type_name, rt.base_price,
                    rt.capacity, r.floor,
                    CASE 
                        WHEN rt.type_name = %s THEN 100  -- Highest score for preferred type
                        WHEN r.floor >= 2 THEN 80       -- Next best for higher floors
                        ELSE 60
                    END as recommendation_score
                FROM rooms r
                JOIN room_types rt ON r.type_id = rt.type_id
                WHERE r.status = 'available'
                AND r.room_id NOT IN (
                    -- This subquery correctly finds rooms that CONFLICT with the dates
                    SELECT room_id FROM bookings
                    WHERE booking_status IN ('confirmed', 'checked-in')
                    AND check_in_date < %s AND check_out_date > %s
                )
                ORDER BY recommendation_score DESC, rt.base_price ASC
                LIMIT 5
            """, (preferred_type, check_out, check_in))
            
            recommendations = cursor.fetchall()
        
        return recommendations
    
    def get_checkout_reminders(self) -> List[Dict]:
        """
        Gets a list of all guests checking out today who are still checked-in.
        """
        # --- MODIFICATION: Using 'with' statement ---
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT 
                    b.booking_id,
                    CONCAT(g.first_name, ' ', g.last_name) as guest_name,
                    g.phone, g.email, r.room_number, b.total_amount,
                    COALESCE(SUM(p.amount), 0) as paid_amount
                FROM bookings b
                JOIN guests g ON b.guest_id = g.guest_id
                JOIN rooms r ON b.room_id = r.room_id
                LEFT JOIN payments p ON b.booking_id = p.booking_id AND p.payment_status = 'completed'
                WHERE b.check_out_date = CURDATE()
                AND b.booking_status = 'checked-in'
                GROUP BY b.booking_id, g.first_name, g.last_name, g.phone, g.email, r.room_number, b.total_amount
            """)
            
            reminders = cursor.fetchall()
        
        # Calculate pending amount in Python
        for reminder in reminders:
            reminder['pending_amount'] = float(reminder['total_amount']) - float(reminder['paid_amount'])
        
        return reminders
    
    def get_cleaning_schedule(self) -> List[Dict]:
        """
        Generates a prioritized list of rooms that need cleaning.
        """
        # --- MODIFICATION: Using 'with' statement ---
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT 
                    r.room_number, rt.type_name, r.floor, r.status,
                    r.last_cleaned,
                    DATEDIFF(NOW(), r.last_cleaned) as days_since_cleaned,
                    CASE 
                        WHEN r.status = 'maintenance' THEN 'High Priority'
                        WHEN DATEDIFF(NOW(), r.last_cleaned) > 3 THEN 'High Priority'
                        WHEN DATEDIFF(NOW(), r.last_cleaned) > 1 THEN 'Medium Priority'
                        ELSE 'Low Priority'
                    END as priority
                FROM rooms r
                JOIN room_types rt ON r.type_id = rt.type_id
                WHERE r.status IN ('available', 'maintenance')
                ORDER BY 
                    CASE priority
                        WHEN 'High Priority' THEN 1
                        WHEN 'Medium Priority' THEN 2
                        ELSE 3
                    END,
                    r.floor, r.room_number
            """)
            
            schedule = cursor.fetchall()
        
        return schedule
    
    def get_advanced_analytics(self) -> Dict:
        """
        Calculates key performance indicators (KPIs) for the hotel.
        """
        # --- MODIFICATION: Using 'with' statement for all queries ---
        with self.connection.cursor(dictionary=True) as cursor:
            
            # --- Monthly Revenue ---
            cursor.execute("""
                SELECT 
                    SUM(amount) as monthly_revenue,
                    COUNT(*) as monthly_transactions,
                    AVG(amount) as avg_transaction
                FROM payments
                WHERE MONTH(payment_date) = MONTH(CURDATE())
                AND YEAR(payment_date) = YEAR(CURDATE())
                AND payment_status = 'completed'
            """)
            monthly_data = cursor.fetchone()
            
            # --- Occupancy ---
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_rooms,
                    SUM(CASE WHEN status = 'occupied' THEN 1 ELSE 0 END) as occupied_rooms
                FROM rooms
            """)
            occupancy = cursor.fetchone()
            
            # --- Top Room Type (by revenue) ---
            cursor.execute("""
                SELECT 
                    rt.type_name, SUM(p.amount) as revenue
                FROM payments p
                JOIN bookings b ON p.booking_id = b.booking_id
                JOIN rooms r ON b.room_id = r.room_id
                JOIN room_types rt ON r.type_id = rt.type_id
                WHERE p.payment_status = 'completed'
                GROUP BY rt.type_name
                ORDER BY revenue DESC
                LIMIT 1
            """)
            top_room = cursor.fetchone()
            
            # --- Guest Retention ---
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT guest_id) as total_guests,
                    SUM(CASE WHEN booking_count > 1 THEN 1 ELSE 0 END) as returning_guests
                FROM (
                    SELECT guest_id, COUNT(*) as booking_count
                    FROM bookings
                    WHERE booking_status = 'checked-out'
                    GROUP BY guest_id
                ) as guest_stats
            """)
            retention = cursor.fetchone()
        
        # --- Calculate Rates in Python (already handles division by zero) ---
        occupancy_rate = (occupancy['occupied_rooms'] / occupancy['total_rooms'] * 100) if occupancy['total_rooms'] > 0 else 0
        retention_rate = (retention['returning_guests'] / retention['total_guests'] * 100) if retention['total_guests'] > 0 else 0
        
        return {
            'monthly_revenue': float(monthly_data['monthly_revenue'] or 0),
            'monthly_transactions': monthly_data['monthly_transactions'],
            'avg_transaction': float(monthly_data['avg_transaction'] or 0),
            'occupancy_rate': round(occupancy_rate, 2),
            'total_rooms': occupancy['total_rooms'],
            'occupied_rooms': occupancy['occupied_rooms'],
            'top_room_type': top_room['type_name'] if top_room else 'N/A',
            'top_room_revenue': float(top_room['revenue'] or 0) if top_room else 0,
            'retention_rate': round(retention_rate, 2),
            'returning_guests': retention['returning_guests'],
            'total_guests': retention['total_guests']
        }
    
    def add_feedback(self, booking_id: int, rating: float, comment: str = None) -> bool:
        """
        Adds guest feedback to a booking.
        """
        # --- MODIFICATION: Using 'with' and 'try/except' ---
        try:
            # Validate rating increments (.0 or .5)
            if rating < 1 or rating > 5 or (rating * 10) % 5 != 0:
                raise ValueError("Rating must be between 1 and 5 in 0.5 steps (e.g., 3.5)")

            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO feedback (booking_id, rating, comment)
                    VALUES (%s, %s, %s)
                """, (booking_id, rating, comment))
            
            # Commit after 'with' block successfully completes
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding feedback: {e}")
            self.connection.rollback() # Rollback changes on error
            return False
    
    def get_average_rating(self) -> float:
        """
        Gets the average guest rating from all feedback.
        """
        # --- MODIFICATION: Using 'with' statement ---
        with self.connection.cursor(dictionary=True) as cursor:
            # Added a 'try' in case feedback table doesn't exist yet
            try:
                cursor.execute("""
                    SELECT AVG(rating) as avg_rating, COUNT(*) as total_reviews
                    FROM feedback
                """)
                result = cursor.fetchone()
            except:
                # If table doesn't exist, return 0
                return {'average_rating': 0.0, 'total_reviews': 0}
        
        return {
            # Original 'or 0' logic is perfect for handling no reviews.
            'average_rating': round(float(result['avg_rating'] or 0), 2),
            'total_reviews': result['total_reviews']
        }
    
    def apply_special_offer(self, booking_id: int, offer_code: str) -> Dict:
        """
        Applies a hard-coded special offer to a booking, updating its total price.
        """
        # Offer logic is fine in Python for this project
        offers = {
            'WEEKEND20': {'discount': 20, 'description': '20% off on weekend bookings'},
            'FIRSTTIME': {'discount': 15, 'description': '15% off for first-time guests'},
            'LOYALTY10': {'discount': 10, 'description': '10% loyalty discount'},
            'EARLYBIRD': {'discount': 12, 'description': '12% off for advance bookings'}
        }
        
        if offer_code not in offers:
            return {'success': False, 'message': 'Invalid offer code'}
        
        offer = offers[offer_code]
        
        # --- MODIFICATION: Using 'with' and 'try/except' for the UPDATE ---
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                
                # --- Get current booking amount ---
                cursor.execute("SELECT total_amount FROM bookings WHERE booking_id = %s", (booking_id,))
                booking = cursor.fetchone()
                
                # --- MODIFICATION: Moved 'None' check inside 'with' block ---
                if not booking:
                    return {'success': False, 'message': 'Booking not found'}
                
                original_amount = float(booking['total_amount'])
                discount_amount = original_amount * (offer['discount'] / 100)
                new_amount = original_amount - discount_amount
                
                # --- Update the booking ---
                cursor.execute("""
                    UPDATE bookings 
                    SET total_amount = %s, special_requests = CONCAT(COALESCE(special_requests, ''), ' | Offer: ', %s)
                    WHERE booking_id = %s
                """, (new_amount, offer_code, booking_id))
            
            # Commit after the 'with' block
            self.connection.commit()
            
            return {
                'success': True, 'message': offer['description'],
                'original_amount': original_amount,
                'discount_amount': round(discount_amount, 2),
                'new_amount': round(new_amount, 2)
            }
        except Exception as e:
            print(f"Error applying special offer: {e}")
            self.connection.rollback() # Rollback the failed UPDATE
            return {'success': False, 'message': f'Database error: {e}'}