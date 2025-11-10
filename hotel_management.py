import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import Optional, List, Dict
import csv
from pathlib import Path
from advanced_features import AdvancedHotelFeatures

class HotelManagementSystem:
    
    def __init__(self, host: str, database: str, user: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Successfully connected to the database")
            self.advanced = AdvancedHotelFeatures(self.connection)
            return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """
        Executes a query that modifies data (INSERT, UPDATE, DELETE).
        MODIFIED: Uses 'with' for cursor and adds rollback on error.
        """
        try:
            # 'with' statement automatically creates AND closes the cursor
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
            
            # Commit after the 'with' block successfully completes
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback() # Rollback changes on error
            return False
    
    def fetch_query(self, query: str, params: tuple = None) -> List:
        """
        Executes a query that fetches data (SELECT).
        MODIFIED: Uses 'with' for cursor.
        """
        try:
            # 'with' statement automatically creates AND closes the cursor
            with self.connection.cursor(dictionary=True) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
    
    def add_guest(self, first_name: str, last_name: str, email: str, phone: str,
                    address: str = None, city: str = None, country: str = None,
                    id_proof_type: str = None, id_proof_number: str = None) -> Optional[int]:
        
        query = """
            INSERT INTO guests (first_name, last_name, email, phone, address, 
                                city, country, id_proof_type, id_proof_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, email, phone, address, city, 
                  country, id_proof_type, id_proof_number)
        
        if self.execute_query(query, params):
            # MODIFIED: Uses 'with' to get the last inserted ID
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT LAST_INSERT_ID()")
                guest_id = cursor.fetchone()[0]
            
            print(f"Guest added successfully! Guest ID: {guest_id}")
            return guest_id
        return None
    
    def search_guest(self, search_term: str) -> List:
        query = """
            SELECT * FROM guests
            WHERE first_name LIKE %s OR last_name LIKE %s 
              OR email LIKE %s OR phone LIKE %s
        """
        search_pattern = f"%{search_term}%"
        return self.fetch_query(query, (search_pattern, search_pattern, 
                                        search_pattern, search_pattern))
    
    def get_guest_by_id(self, guest_id: int) -> Optional[Dict]:
        query = "SELECT * FROM guests WHERE guest_id = %s"
        results = self.fetch_query(query, (guest_id,))
        return results[0] if results else None
    
    def get_available_rooms(self, check_in: date, check_out: date, room_type: str = None, hotel_id: int = None) -> List:
        query = """
            SELECT r.room_id, r.room_number, rt.type_name, rt.base_price, 
                   rt.capacity, r.floor, h.hotel_name, h.location, h.city
            FROM rooms r
            JOIN room_types rt ON r.type_id = rt.type_id
            JOIN hotels h ON r.hotel_id = h.hotel_id
            WHERE r.status = 'available'
            AND r.room_id NOT IN (
                SELECT room_id FROM bookings
                WHERE booking_status IN ('confirmed', 'checked-in')
                AND check_in_date < %s AND check_out_date > %s
            )
        """
        
        params = [check_out, check_in]
        
        if hotel_id:
            query += " AND r.hotel_id = %s"
            params.append(hotel_id)
        
        if room_type:
            query += " AND rt.type_name = %s"
            params.append(room_type)
        
        return self.fetch_query(query, tuple(params))
    
    def get_all_rooms(self) -> List:
        query = """
            SELECT r.room_id, r.room_number, rt.type_name, rt.base_price,
                   r.floor, r.status
            FROM rooms r
            JOIN room_types rt ON r.type_id = rt.type_id
            ORDER BY r.room_number
        """
        return self.fetch_query(query)
    
    def update_room_status(self, room_id: int, status: str) -> bool:
        query = "UPDATE rooms SET status = %s WHERE room_id = %s"
        return self.execute_query(query, (status, room_id))
    
    def create_booking(self, guest_id: int, room_id: int, check_in: date,
                       check_out: date, num_adults: int = 1, num_children: int = 0,
                       special_requests: str = None) -> Optional[int]:
        
        query = "SELECT base_price FROM room_types WHERE type_id = (SELECT type_id FROM rooms WHERE room_id = %s)"
        result = self.fetch_query(query, (room_id,))
        
        if not result:
            print("Room not found")
            return None
        
        base_price = float(result[0]['base_price'])
        # Handle date objects vs. string
        try:
            if isinstance(check_in, str):
                check_in_date_obj = datetime.strptime(check_in, '%Y-%m-%d').date()
            else:
                check_in_date_obj = check_in
            
            if isinstance(check_out, str):
                check_out_date_obj = datetime.strptime(check_out, '%Y-%m-%d').date()
            else:
                check_out_date_obj = check_out
                
            days = (check_out_date_obj - check_in_date_obj).days
        except Exception as e:
            print(f"Error with dates: {e}. Ensure format is YYYY-MM-DD.")
            return None

        total_amount = base_price * days
        
        query = """
            INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date,
                                  num_adults, num_children, total_amount, special_requests)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (guest_id, room_id, check_in, check_out, num_adults, 
                  num_children, total_amount, special_requests)
        
        if self.execute_query(query, params):
            self.update_room_status(room_id, 'reserved')
            
            # MODIFIED: Uses 'with' to get the last inserted ID
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT LAST_INSERT_ID()")
                booking_id = cursor.fetchone()[0]
            
            print(f"Booking created successfully! Booking ID: {booking_id}")
            print(f"Total Amount: ₹{total_amount}")
            return booking_id
        return None
    
    def check_in_guest(self, booking_id: int) -> bool:
        query = """
            UPDATE bookings 
            SET booking_status = 'checked-in', actual_check_in = NOW()
            WHERE booking_id = %s
        """
        if self.execute_query(query, (booking_id,)):
            room_query = "SELECT room_id FROM bookings WHERE booking_id = %s"
            result = self.fetch_query(room_query, (booking_id,))
            if result:
                self.update_room_status(result[0]['room_id'], 'occupied')
            print(f"Check-in successful for booking {booking_id}")
            return True
        return False
    
    def check_out_guest(self, booking_id: int) -> bool:
        query = """
            UPDATE bookings 
            SET booking_status = 'checked-out', actual_check_out = NOW()
            WHERE booking_id = %s
        """
        if self.execute_query(query, (booking_id,)):
            room_query = "SELECT room_id FROM bookings WHERE booking_id = %s"
            result = self.fetch_query(room_query, (booking_id,))
            if result:
                # MODIFICATION: Set to 'maintenance' (for cleaning) instead of 'available'
                self.update_room_status(result[0]['room_id'], 'maintenance')
            print(f"Check-out successful for booking {booking_id}. Room sent for cleaning.")
            return True
        return False
    
    def cancel_booking(self, booking_id: int) -> bool:
        query = "UPDATE bookings SET booking_status = 'cancelled' WHERE booking_id = %s"
        if self.execute_query(query, (booking_id,)):
            room_query = "SELECT room_id FROM bookings WHERE booking_id = %s"
            result = self.fetch_query(room_query, (booking_id,))
            if result:
                self.update_room_status(result[0]['room_id'], 'available')
            print(f"Booking {booking_id} cancelled successfully")
            return True
        return False
    
    def get_booking_details(self, booking_id: int) -> Optional[Dict]:
        query = """
            SELECT b.*, g.first_name, g.last_name, g.phone, g.email,
                   r.room_number, rt.type_name
            FROM bookings b
            JOIN guests g ON b.guest_id = g.guest_id
            JOIN rooms r ON b.room_id = r.room_id
            JOIN room_types rt ON r.type_id = rt.type_id
            WHERE b.booking_id = %s
        """
        results = self.fetch_query(query, (booking_id,))
        return results[0] if results else None

    def get_booking_full_details(self, booking_id: int) -> Optional[Dict]:
        """Return comprehensive booking info including payments and feedback."""
        booking = self.get_booking_details(booking_id)
        if not booking:
            return None

        # Payments summary
        payments = self.fetch_query(
            """
            SELECT payment_id, amount, payment_method, payment_status, payment_date, transaction_id
            FROM payments
            WHERE booking_id = %s
            ORDER BY payment_date ASC
            """, (booking_id,)
        )
        total_paid_row = self.fetch_query(
            """SELECT COALESCE(SUM(amount),0) AS total_paid
                FROM payments WHERE booking_id = %s AND payment_status='completed'""",
            (booking_id,)
        )
        total_paid = float(total_paid_row[0]['total_paid']) if total_paid_row else 0.0
        balance = float(booking['total_amount']) - total_paid

        # Feedback list & average
        feedback_list = self.fetch_query(
            """
            SELECT rating, comment, feedback_date
            FROM feedback
            WHERE booking_id = %s
            ORDER BY feedback_date DESC
            """, (booking_id,)
        )
        avg_row = self.fetch_query(
            """SELECT ROUND(AVG(rating),2) AS avg_rating, COUNT(*) AS count
                FROM feedback WHERE booking_id = %s""",
            (booking_id,)
        )
        avg_rating = float(avg_row[0]['avg_rating'] or 0) if avg_row else 0.0
        feedback_count = int(avg_row[0]['count'] or 0) if avg_row else 0

        return {
            'booking': booking,
            'payments': payments,
            'total_paid': round(total_paid,2),
            'balance': round(balance,2),
            'feedback': feedback_list,
            'avg_rating': avg_rating,
            'feedback_count': feedback_count
        }
    
    def get_current_checkins(self) -> List:
        query = """
            SELECT b.booking_id, g.first_name, g.last_name, g.phone,
                   r.room_number, rt.type_name, b.check_in_date, b.check_out_date
            FROM bookings b
            JOIN guests g ON b.guest_id = g.guest_id
            JOIN rooms r ON b.room_id = r.room_id
            JOIN room_types rt ON r.type_id = rt.type_id
            WHERE b.booking_status = 'checked-in'
            ORDER BY r.room_number
        """
        return self.fetch_query(query)
    
    def add_payment(self, booking_id: int, amount: float, payment_method: str,
                      transaction_id: str = None) -> Optional[int]:
        query = """
            INSERT INTO payments (booking_id, amount, payment_method, transaction_id)
            VALUES (%s, %s, %s, %s)
        """
        params = (booking_id, amount, payment_method, transaction_id)
        
        if self.execute_query(query, params):
            # MODIFIED: Uses 'with' to get the last inserted ID
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT LAST_INSERT_ID()")
                payment_id = cursor.fetchone()[0]
            
            print(f"Payment recorded successfully! Payment ID: {payment_id}")
            return payment_id
        return None
    
    def get_booking_payments(self, booking_id: int) -> List:
        query = """
            SELECT * FROM payments 
            WHERE booking_id = %s AND payment_status = 'completed'
            ORDER BY payment_date DESC
        """
        return self.fetch_query(query, (booking_id,))
    
    def get_all_hotels(self) -> List:
        """Get list of all hotels with location information."""
        query = """
            SELECT hotel_id, hotel_name, location, address, city, state, country,
                   phone, email, rating, description
            FROM hotels
            ORDER BY hotel_name
        """
        return self.fetch_query(query)
    
    def get_hotel_by_id(self, hotel_id: int) -> Optional[Dict]:
        """Get details of a specific hotel."""
        query = "SELECT * FROM hotels WHERE hotel_id = %s"
        results = self.fetch_query(query, (hotel_id,))
        return results[0] if results else None
    
    def get_occupancy_report(self) -> List:
        query = """
            SELECT 
                rt.type_name,
                COUNT(r.room_id) AS total_rooms,
                SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) AS occupied,
                SUM(CASE WHEN r.status = 'available' THEN 1 ELSE 0 END) AS available,
                SUM(CASE WHEN r.status = 'maintenance' THEN 1 ELSE 0 END) AS in_maintenance,
                ROUND((SUM(CASE WHEN r.status = 'occupied' THEN 1 ELSE 0 END) / 
                       COUNT(r.room_id)) * 100, 2) AS occupancy_rate
            FROM rooms r
            JOIN room_types rt ON r.type_id = rt.type_id
            GROUP BY rt.type_name
        """
        return self.fetch_query(query)
    
    def get_revenue_report(self, start_date: date = None, end_date: date = None) -> Optional[Dict]:
        if start_date and end_date:
            query = """
                SELECT 
                    COUNT(*) AS total_transactions,
                    SUM(amount) AS total_revenue,
                    AVG(amount) AS avg_transaction
                FROM payments
                WHERE payment_status = 'completed'
                AND DATE(payment_date) BETWEEN %s AND %s
            """
            params = (start_date, end_date)
        else:
            query = """
                SELECT 
                    COUNT(*) AS total_transactions,
                    SUM(amount) AS total_revenue,
                    AVG(amount) AS avg_transaction
                FROM payments
                WHERE payment_status = 'completed'
            """
            params = None
        
        results = self.fetch_query(query, params)
        return results[0] if results else None

    def export_to_csv(self, table_name: str, filename: str = None) -> bool:
        """Export data from a table to CSV file."""
        try:
            export_dir = Path("exports")
            export_dir.mkdir(exist_ok=True)

            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{table_name}_{timestamp}.csv"

            filepath = export_dir / filename
            data = self.fetch_query(f"SELECT * FROM {table_name}")
            if not data:
                print(f"No data found in {table_name} table.")
                return False

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    processed_row = {}
                    for key, value in row.items():
                        if isinstance(value, (datetime, date)):
                            processed_row[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            processed_row[key] = value
                    writer.writerow(processed_row)
            print(f"✓ Exported {len(data)} records to {filepath}")
            return True
        except Error as e:
            print(f"Database error during export: {e}")
            return False
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def export_all_data(self) -> bool:
        """Export all tables to CSV files in exports folder."""
        tables = ['hotels', 'departments', 'staff', 'room_types', 'rooms',
                  'guests', 'bookings', 'payments', 'feedback']
        print("\n" + "="*60)
        print("   EXPORTING ALL DATA TO CSV")
        print("="*60)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        success_count = 0
        for table in tables:
            print(f"\nExporting {table}...", end=" ")
            if self.export_to_csv(table, f"{table}_{timestamp}.csv"):
                success_count += 1
        print("\n" + "="*60)
        print(f"✓ Successfully exported {success_count}/{len(tables)} tables")
        print(f"📁 Files saved in: exports\\")
        print("="*60)
        return success_count == len(tables)

    def export_custom_query(self, query: str, filename: str) -> bool:
        """Export results of a custom query to CSV."""
        try:
            export_dir = Path("exports")
            export_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = export_dir / f"{filename}_{timestamp}.csv"
            data = self.fetch_query(query)
            if not data:
                print("No data returned from query.")
                return False
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    processed_row = {}
                    for key, value in row.items():
                        if isinstance(value, (datetime, date)):
                            processed_row[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            processed_row[key] = value
                    writer.writerow(processed_row)
            print(f"✓ Exported {len(data)} records to {filepath}")
            return True
        except Exception as e:
            print(f"Error exporting custom query: {e}")
            return False

def render_stars(rating: float, max_stars: int = 5) -> str:
    """Return a star string with half-star support for a given rating.
    Uses ★ for full, ⯪ for half, and ☆ for empty.
    """
    try:
        rating = float(rating)
    except Exception:
        rating = 0.0
    if rating < 0:
        rating = 0.0
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = max_stars - full - half
    return ("★" * full) + ("⯪" * half) + ("☆" * max(0, empty))


def print_menu():
    print("\n" + "="*60)
    print("   HOTEL MANAGEMENT SYSTEM - PREMIUM EDITION")
    print("="*60)
    print("BASIC OPERATIONS:")
    print("1.  Add New Guest")
    print("2.  Search Guest")
    print("3.  View Available Rooms")
    print("4.  Create Booking")
    print("5.  Check-in Guest")
    print("6.  Check-out Guest")
    print("7.  View Current Check-ins")
    print("8.  Cancel Booking")
    print("9.  Add Payment")
    print("10. View Booking Details")
    print("\nADVANCED FEATURES:")
    print("11. Check Guest Loyalty Status")
    print("12. Get Room Recommendations (AI)")
    print("13. Apply Special Offer Code")
    print("14. Checkout Reminders for Today")
    print("15. Housekeeping Schedule")
    print("16. Add Guest Feedback")
    print("\nHOTEL LOCATIONS:")
    print("17. View All Hotels & Locations")
    print("18. Search Rooms by Hotel")
    print("\nREPORTS & ANALYTICS:")
    print("19. Occupancy Report")
    print("20. Revenue Report")
    print("21. Advanced Business Analytics")
    print("22. Hotel Rating & Reviews")
    print("\nDATA EXPORT:")
    print("23. Export All Data to CSV")
    print("24. Export Single Table to CSV")
    print("25. Export Active Bookings Report")
    print("\n0.  Exit")
    print("="*60)


def main():
    HOST = "localhost"
    DATABASE = "hotel_management" # Make sure this DB exists
    USER = "root"
    PASSWORD = "Souvik@007" # <-- IMPORTANT: Change this
    
    hotel = HotelManagementSystem(HOST, DATABASE, USER, PASSWORD)
    
    if not hotel.connect():
        print("Failed to connect to database. Exiting...")
        return
    
    try:
        while True:
            print_menu()
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                print("\n--- Add New Guest ---")
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                address = input("Address (optional): ")
                city = input("City (optional): ")
                country = input("Country (optional): ")
                id_proof_type = input("ID Proof Type (optional): ")
                id_proof_number = input("ID Proof Number (optional): ")
                
                hotel.add_guest(first_name, last_name, email, phone, address,
                              city, country, id_proof_type, id_proof_number)
            
            elif choice == "2":
                # Search Guest
                search_term = input("\nEnter name, email, or phone to search: ")
                guests = hotel.search_guest(search_term)
                
                if guests:
                    print(f"\nFound {len(guests)} guest(s):")
                    for guest in guests:
                        print(f"\nGuest ID: {guest['guest_id']}")
                        print(f"Name: {guest['first_name']} {guest['last_name']}")
                        print(f"Email: {guest['email']}")
                        print(f"Phone: {guest['phone']}")
                else:
                    print("No guests found")
            
            elif choice == "3":
                # View Available Rooms
                try:
                    check_in = input("Check-in date (YYYY-MM-DD): ")
                    check_out = input("Check-out date (YYYY-MM-DD): ")
                    
                    # Ask if user wants to filter by hotel
                    filter_hotel = input("Filter by hotel? (y/n): ").lower()
                    hotel_id = None
                    if filter_hotel == 'y':
                        hotels = hotel.get_all_hotels()
                        print("\nAvailable Hotels:")
                        for h in hotels:
                            print(f"{h['hotel_id']}. {h['hotel_name']} - {h['location']}, {h['city']}")
                        hotel_id = int(input("Enter Hotel ID: "))
                    
                    rooms = hotel.get_available_rooms(check_in, check_out, hotel_id=hotel_id)
                    
                    if rooms:
                        print(f"\n{len(rooms)} room(s) available:")
                        for room in rooms:
                            print(f"\n🏨 Hotel: {room['hotel_name']} ({room['location']}, {room['city']})")
                            print(f"Room ID: {room['room_id']} | Room Number: {room['room_number']} - {room['type_name']}")
                            print(f"Price: ₹{room['base_price']}/night")
                            print(f"Capacity: {room['capacity']} persons | Floor: {room['floor']}")
                    else:
                        print("No rooms available for selected dates")
                except Exception as e:
                    print(f"Error: {e}. Please use YYYY-MM-DD format.")
            
            elif choice == "4":
                # Create Booking
                try:
                    print("\n--- Create Booking ---")
                    guest_id = int(input("Guest ID: "))
                    room_id = int(input("Room ID: "))
                    check_in = input("Check-in date (YYYY-MM-DD): ")
                    check_out = input("Check-out date (YYYY-MM-DD): ")
                    num_adults = int(input("Number of adults: "))
                    num_children = int(input("Number of children: "))
                    special_requests = input("Special requests (optional): ")
                    
                    hotel.create_booking(guest_id, room_id, check_in, check_out,
                                         num_adults, num_children, special_requests)
                except ValueError:
                    print("Error: Please enter valid numbers for IDs and guest counts")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == "5":
                # Check-in
                try:
                    booking_id = int(input("\nEnter Booking ID for check-in: "))
                    hotel.check_in_guest(booking_id)
                except ValueError:
                    print("Error: Please enter a valid booking ID")
            
            elif choice == "6":
                # Check-out
                try:
                    booking_id = int(input("\nEnter Booking ID for check-out: "))
                    hotel.check_out_guest(booking_id)
                except ValueError:
                    print("Error: Please enter a valid booking ID")
            
            elif choice == "7":
                # Current Check-ins
                checkins = hotel.get_current_checkins()
                
                if checkins:
                    print(f"\n{len(checkins)} guest(s) currently checked in:")
                    for booking in checkins:
                        print(f"\nRoom {booking['room_number']} - {booking['type_name']}")
                        print(f"Guest: {booking['first_name']} {booking['last_name']}")
                        print(f"Phone: {booking['phone']}")
                        print(f"Check-out: {booking['check_out_date']}")
                else:
                    print("No guests currently checked in")
            
            elif choice == "8":
                # Cancel Booking
                try:
                    booking_id = int(input("\nEnter Booking ID to cancel: "))
                    hotel.cancel_booking(booking_id)
                except ValueError:
                    print("Error: Please enter a valid booking ID")
            
            elif choice == "9":
                # Add Payment
                try:
                    print("\n--- Add Payment ---")
                    booking_id = int(input("Booking ID: "))
                    amount = float(input("Amount: "))
                    print("Payment Methods: cash, credit_card, debit_card, upi, net_banking")
                    payment_method = input("Payment Method: ")
                    transaction_id = input("Transaction ID (optional): ")
                    
                    hotel.add_payment(booking_id, amount, payment_method, 
                                      transaction_id if transaction_id else None)
                except ValueError:
                    print("Error: Please enter valid numbers for booking ID and amount")
            
            elif choice == "10":
                # View Booking Details (Full)
                try:
                    booking_id = int(input("\nEnter Booking ID: "))
                    details = hotel.get_booking_full_details(booking_id)
                    
                    if details:
                        b = details['booking']
                        print("\n=== BOOKING DETAILS ===")
                        print(f"Booking ID: {b['booking_id']}  | Status: {b['booking_status']}")
                        print(f"Guest: {b['first_name']} {b['last_name']}  | Phone: {b['phone']}  | Email: {b['email']}")
                        print(f"Room: {b['room_number']} - {b['type_name']}")
                        print(f"Check-in: {b['check_in_date']}  | Check-out: {b['check_out_date']}")
                        if b.get('special_requests'):
                            print(f"Special Requests: {b['special_requests']}")
                        print("\n--- FINANCIALS ---")
                        print(f"Total Amount: ₹{float(b['total_amount']):.2f}")
                        print(f"Total Paid:   ₹{details['total_paid']:.2f}")
                        print(f"Balance:      ₹{details['balance']:.2f}")
                        
                        print("\n--- PAYMENTS ---")
                        if details['payments']:
                            for p in details['payments']:
                                print(f"#{p['payment_id']}  {p['payment_date']}  ₹{float(p['amount']):.2f}  {p['payment_method']}  {p['payment_status']}")
                        else:
                            print("No payments recorded yet.")
                        
                        print("\n--- FEEDBACK ---")
                        if details['feedback']:
                            print(f"Average: {details['avg_rating']}/5.0 {render_stars(details['avg_rating'])}  ({details['feedback_count']} review(s))")
                            for f in details['feedback']:
                                print(f"{f['feedback_date']}: {f['rating']}/5 {render_stars(f['rating'])} - {f['comment'] or ''}")
                        else:
                            print("No feedback yet.")
                    else:
                        print("Booking not found")
                except ValueError:
                    print("Error: Please enter a valid booking ID")
            
            elif choice == "11":
                # Guest Loyalty Status
                try:
                    guest_id = int(input("\nEnter Guest ID: "))
                    loyalty = hotel.advanced.get_guest_loyalty_tier(guest_id)
                    
                    print(f"\n{'='*50}")
                    print(f"🌟 GUEST LOYALTY STATUS")
                    print(f"{'='*50}")
                    print(f"Tier: {loyalty['tier']}")
                    print(f"Discount: {loyalty['discount']}%")
                    print(f"Total Bookings: {loyalty['bookings']}")
                    print(f"Total Spent: ₹{loyalty['spent']:.2f}")
                    print(f"Benefits: {loyalty['benefits']}")
                    print(f"{'='*50}")
                except ValueError:
                    print("Error: Please enter a valid guest ID")
            
            elif choice == "12":
                # AI Room Recommendations
                try:
                    guest_id = int(input("\nEnter Guest ID: "))
                    check_in = input("Check-in date (YYYY-MM-DD): ")
                    check_out = input("Check-out date (YYYY-MM-DD): ")
                    
                    recommendations = hotel.advanced.recommend_rooms(guest_id, check_in, check_out)
                    
                    if recommendations:
                        print(f"\n🤖 AI-POWERED ROOM RECOMMENDATIONS")
                        print(f"Based on your previous stays, we recommend:")
                        for i, room in enumerate(recommendations, 1):
                            print(f"\n{i}. Room {room['room_number']} - {room['type_name']}")
                            print(f"   Price: ₹{room['base_price']}/night")
                            print(f"   Floor: {room['floor']} | Recommendation Score: {room['recommendation_score']}/100")
                    else:
                        print("No recommendations available")
                except ValueError:
                    print("Error: Please enter valid inputs")
            
            elif choice == "13":
                # Apply Special Offer
                try:
                    booking_id = int(input("\nEnter Booking ID: "))
                    print("\nAvailable Offers:")
                    print("- WEEKEND20: 20% off on weekend bookings")
                    print("- FIRSTTIME: 15% off for first-time guests")
                    print("- LOYALTY10: 10% loyalty discount")
                    print("- EARLYBIRD: 12% off for advance bookings")
                    
                    offer_code = input("\nEnter Offer Code: ").upper()
                    result = hotel.advanced.apply_special_offer(booking_id, offer_code)
                    
                    if result['success']:
                        print(f"\n✅ {result['message']}")
                        print(f"Original Amount: ₹{result['original_amount']:.2f}")
                        print(f"Discount: ₹{result['discount_amount']:.2f}")
                        print(f"New Amount: ₹{result['new_amount']:.2f}")
                    else:
                        print(f"\n❌ {result['message']}")
                except ValueError:
                    print("Error: Please enter a valid booking ID")
            
            elif choice == "14":
                # Checkout Reminders
                reminders = hotel.advanced.get_checkout_reminders()
                
                if reminders:
                    print(f"\n📅 CHECKOUT REMINDERS FOR TODAY ({datetime.now().strftime('%Y-%m-%d')})")
                    print(f"{'='*70}")
                    for r in reminders:
                        print(f"\nRoom {r['room_number']} - {r['guest_name']}")
                        print(f"Phone: {r['phone']} | Email: {r['email']}")
                        print(f"Total: ₹{r['total_amount']:.2f} | Paid: ₹{r['paid_amount']:.2f}")
                        if r['pending_amount'] > 0:
                            print(f"⚠️ PENDING: ₹{r['pending_amount']:.2f}")
                        else:
                            print("✅ Fully Paid")
                else:
                    print("\nNo checkouts scheduled for today")
            
            elif choice == "15":
                # Housekeeping Schedule
                schedule = hotel.advanced.get_cleaning_schedule()
                
                if schedule:
                    print(f"\n🧹 HOUSEKEEPING SCHEDULE FOR TODAY")
                    print(f"{'='*80}")
                    print(f"{'Room':<10} {'Type':<15} {'Floor':<8} {'Status':<15} {'Priority':<15}")
                    print(f"{'-'*80}")
                    
                    for room in schedule:
                        print(f"{room['room_number']:<10} {room['type_name']:<15} {room['floor']:<8} "
                              f"{room['status']:<15} {room['priority']:<15}")
                else:
                    print("\nNo rooms need cleaning today")
            
            elif choice == "16":
                # Add Feedback
                try:
                    booking_id = int(input("\nEnter Booking ID: "))
                    rating_input = input("Rating (1 - 5, can use .5 like 4.5): ")
                    rating = float(rating_input)
                    
                    if rating < 1 or rating > 5 or (rating * 10) % 5 != 0:
                        print("Error: Rating must be between 1 and 5 in 0.5 steps (e.g., 3.5)")
                    else:
                        comment = input("Comment (optional): ")
                        if hotel.advanced.add_feedback(booking_id, rating, comment):
                            print(f"\n✅ Thank you for your feedback! Rating: {rating} {render_stars(rating)}")
                        else:
                            print("Error adding feedback")
                except ValueError:
                    print("Error: Please enter valid numbers")
            
            elif choice == "17":
                # View All Hotels & Locations
                hotels = hotel.get_all_hotels()
                
                if hotels:
                    print("\n" + "="*80)
                    print("🏨 ALL HOTEL LOCATIONS")
                    print("="*80)
                    for h in hotels:
                        print(f"\n📍 {h['hotel_name']}")
                        print(f"   Location: {h['location']}, {h['city']}, {h['state']}, {h['country']}")
                        print(f"   Address: {h['address']}")
                        print(f"   Phone: {h['phone']} | Email: {h['email']}")
                        print(f"   Rating: {h['rating']}/5.0 {render_stars(h['rating'])}")
                        if h['description']:
                            print(f"   About: {h['description']}")
                else:
                    print("No hotels found")
            
            elif choice == "18":
                # Search Rooms by Hotel
                try:
                    hotels = hotel.get_all_hotels()
                    print("\n--- Select Hotel ---")
                    for h in hotels:
                        print(f"{h['hotel_id']}. {h['hotel_name']} - {h['location']}, {h['city']}")
                    
                    hotel_id = int(input("\nEnter Hotel ID: "))
                    check_in = input("Check-in date (YYYY-MM-DD): ")
                    check_out = input("Check-out date (YYYY-MM-DD): ")
                    
                    rooms = hotel.get_available_rooms(check_in, check_out, hotel_id=hotel_id)
                    
                    if rooms:
                        print(f"\n✅ {len(rooms)} room(s) available at {rooms[0]['hotel_name']}:")
                        for room in rooms:
                            print(f"\n   Room {room['room_number']} - {room['type_name']}")
                            print(f"   Price: ₹{room['base_price']}/night | Floor: {room['floor']} | Capacity: {room['capacity']}")
                    else:
                        print("No rooms available for selected dates at this hotel")
                except ValueError:
                    print("Error: Please enter valid hotel ID")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == "19":
                # Occupancy Report
                report = hotel.get_occupancy_report()
                
                if report:
                    print("\n--- Room Occupancy Report ---")
                    for row in report:
                        print(f"\n{row['type_name']}:")
                        print(f"  Total Rooms: {row['total_rooms']}")
                        print(f"  Occupied: {row['occupied']}")
                        print(f"  Available: {row['available']}")
                        print(f"  In Maintenance: {row['in_maintenance']}")
                        print(f"  Occupancy Rate: {row['occupancy_rate']}%")
            
            elif choice == "20":
                # Revenue Report
                report = hotel.get_revenue_report()
                
                if report:
                    print("\n--- Revenue Report (All Time) ---")
                    print(f"Total Transactions: {report['total_transactions']}")
                    print(f"Total Revenue: ₹{float(report['total_revenue'] or 0):.2f}")
                    print(f"Average Transaction: ₹{float(report['avg_transaction'] or 0):.2f}")
            
            elif choice == "21":
                # Advanced Analytics
                analytics = hotel.advanced.get_advanced_analytics()
                
                print(f"\n{'='*70}")
                print(f"📊 ADVANCED BUSINESS ANALYTICS")
                print(f"{'='*70}")
                print(f"\n💰 REVENUE METRICS:")
                print(f"   Monthly Revenue: ₹{analytics['monthly_revenue']:.2f}")
                print(f"   Transactions: {analytics['monthly_transactions']}")
                print(f"   Average Transaction: ₹{analytics['avg_transaction']:.2f}")
                
                print(f"\n🏨 OCCUPANCY METRICS:")
                print(f"   Occupancy Rate: {analytics['occupancy_rate']}%")
                print(f"   Occupied Rooms: {analytics['occupied_rooms']}/{analytics['total_rooms']}")
                
                print(f"\n🎯 PERFORMANCE METRICS:")
                print(f"   Top Room Type: {analytics['top_room_type']}")
                print(f"   Top Room Revenue: ₹{analytics['top_room_revenue']:.2f}")
                print(f"   Guest Retention: {analytics['retention_rate']}%")
                print(f"   Returning Guests: {analytics['returning_guests']}/{analytics['total_guests']}")
                print(f"{'='*70}")
            
            elif choice == "22":
                # Hotel Rating
                rating_data = hotel.advanced.get_average_rating()
                
                print(f"\n{'='*50}")
                print(f"⭐ HOTEL RATING & REVIEWS")
                print(f"{'='*50}")
                rating = rating_data['average_rating']
                print(f"Average Rating: {rating}/5.0 {render_stars(rating)}")
                print(f"Total Reviews: {rating_data['total_reviews']}")
                print(f"{'='*50}")
            
            elif choice == "23":
                # Export All Data
                print("\n--- Export All Data to CSV ---")
                confirm = input("This will export all tables to CSV files. Continue? (y/n): ")
                if confirm.lower() == 'y':
                    hotel.export_all_data()
            
            elif choice == "24":
                # Export Single Table
                print("\n--- Export Single Table ---")
                print("Available tables:")
                print("1. hotels        2. departments  3. staff        4. room_types")
                print("5. rooms         6. guests       7. bookings     8. payments")
                print("9. feedback")
                
                table_choice = input("\nEnter table number: ")
                tables = ['hotels', 'departments', 'staff', 'room_types', 'rooms',
                         'guests', 'bookings', 'payments', 'feedback']
                
                try:
                    table_idx = int(table_choice) - 1
                    if 0 <= table_idx < len(tables):
                        table_name = tables[table_idx]
                        hotel.export_to_csv(table_name)
                    else:
                        print("Invalid table number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            elif choice == "25":
                # Export Active Bookings Report
                print("\n--- Export Active Bookings Report ---")
                query = """
                    SELECT 
                        b.booking_id,
                        CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
                        g.email,
                        g.phone,
                        r.room_number,
                        rt.type_name AS room_type,
                        b.check_in_date,
                        b.check_out_date,
                        b.num_adults,
                        b.num_children,
                        b.booking_status,
                        b.total_amount
                    FROM bookings b
                    JOIN guests g ON b.guest_id = g.guest_id
                    JOIN rooms r ON b.room_id = r.room_id
                    JOIN room_types rt ON r.type_id = rt.type_id
                    WHERE b.booking_status IN ('confirmed', 'checked_in')
                    ORDER BY b.check_in_date
                """
                hotel.export_custom_query(query, "active_bookings_report")
            
            elif choice == "0":
                print("\nThank you for using Hotel Management System!")
                break
            
            else:
                print("\nInvalid choice. Please try again.")
    
    except Exception as e:
        print(f"A critical error occurred: {e}")
    finally:
        hotel.disconnect()


if __name__ == "__main__":
    main()