# Hotel Management System

A comprehensive multi-hotel management system with location-based search, loyalty programs, and advanced analytics.

## Key Features

### 🏨 Multi-Hotel Support
- Manage multiple hotel properties from a single system
- 3 hotels in Barasat, Kolkata, West Bengal:
  - **Grand Palace Hotel** - Barasat Station Area
  - **Seaborn Resort** - Madhyamgram
  - **Anand Lodge** - New Barrackpore

### 📍 Location-Based Search
- Search hotels by location (Option 18)
- Filter available rooms by specific hotel (Option 19)
- View all hotels with full location details (Option 17)
- Search by area (e.g., "Station Area", "Madhyamgram", "Barasat")

### ⭐ Half-Star Rating System
- Support for half-star ratings (3.5, 4.5 out of 5)
- Visual star display with ★ (full), ⯪ (half), ☆ (empty)
- Guest feedback with ratings and comments

### 💼 Advanced Features
- Guest loyalty tiers (Bronze, Silver, Gold, Platinum)
- AI-powered room recommendations
- Dynamic pricing with special offers
- Comprehensive booking details with payment history
- Real-time occupancy and revenue reports
- Housekeeping schedules and checkout reminders

### 📊 Data Export
- Export all data to CSV (Option 24)
- Export individual tables (Option 25)
- Export custom reports (Option 26)
- Active bookings report

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for installation instructions.

## Database Schema

The system uses 9 tables:
1. **hotels** - Hotel properties with location information
2. **departments** - Hotel departments
3. **staff** - Staff members assigned to hotels
4. **room_types** - Room categories and pricing
5. **rooms** - Individual rooms per hotel
6. **guests** - Guest information
7. **bookings** - Reservations and bookings
8. **payments** - Payment transactions
9. **feedback** - Guest reviews and ratings

## Menu Options

### Basic Operations (1-10)
- Guest management (add, search)
- Room availability and booking
- Check-in/check-out
- Payment processing
- Booking details with payment history

### Advanced Features (11-16)
- Loyalty status tracking
- AI room recommendations
- Special offer codes
- Housekeeping schedules
- Guest feedback with half-star ratings

### Hotel Locations (17-19)
- **17:** View All Hotels & Locations
- **18:** Search Hotels by Location
- **19:** Search Rooms by Hotel

### Reports & Analytics (20-23)
- Occupancy reports
- Revenue analytics
- Advanced business metrics
- Hotel ratings and reviews

### Data Export (24-26)
- Export all tables to CSV
- Export single table
- Export active bookings report

## Technologies

- **Python 3.7+**
- **MySQL 5.7+**
- **mysql-connector-python**

## Testing

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing scenarios.

## ER Diagram

See [ER_DIAGRAM.md](ER_DIAGRAM.md) for the complete entity-relationship diagram.
For a visual Mermaid diagram, see [ER_DIAGRAM_MERMAID.md](ER_DIAGRAM_MERMAID.md).
