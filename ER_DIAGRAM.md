# Entity-Relationship (ER) Diagram
## Hotel Management System

---

## Entities and Attributes

### 1. DEPARTMENTS
**Primary Key:** department_id
- department_id (PK)
- department_name
- description

### 2. STAFF
**Primary Key:** staff_id  
**Foreign Key:** department_id → DEPARTMENTS
- staff_id (PK)
- first_name
- last_name
- email (UNIQUE)
- phone
- department_id (FK)
- position
- salary
- hire_date
- status (active/inactive)

### 3. ROOM_TYPES
**Primary Key:** type_id
- type_id (PK)
- type_name
- description
- base_price
- capacity

### 4. ROOMS
**Primary Key:** room_id  
**Foreign Key:** type_id → ROOM_TYPES
- room_id (PK)
- room_number (UNIQUE)
- type_id (FK)
- floor
- status (available/occupied/maintenance/reserved)
- last_cleaned

### 5. GUESTS
**Primary Key:** guest_id
- guest_id (PK)
- first_name
- last_name
- email (UNIQUE)
- phone
- address
- city
- country
- id_proof_type
- id_proof_number
- registration_date

### 6. BOOKINGS
**Primary Key:** booking_id  
**Foreign Keys:** guest_id → GUESTS, room_id → ROOMS
- booking_id (PK)
- guest_id (FK)
- room_id (FK)
- check_in_date
- check_out_date
- actual_check_in
- actual_check_out
- num_adults
- num_children
- booking_status (confirmed/checked-in/checked-out/cancelled)
- total_amount
- special_requests
- booking_date

### 7. PAYMENTS
**Primary Key:** payment_id  
**Foreign Key:** booking_id → BOOKINGS
- payment_id (PK)
- booking_id (FK)
- amount
- payment_date
- payment_method (cash/credit_card/debit_card/upi/net_banking)
- payment_status (pending/completed/refunded)
- transaction_id

### 8. FEEDBACK
**Primary Key:** feedback_id  
**Foreign Key:** booking_id → BOOKINGS
- feedback_id (PK)
- booking_id (FK)
- rating (DECIMAL(2,1), 1.0–5.0 in 0.5 steps)
- comment (TEXT)
- feedback_date (DATETIME)

<!-- Removed duplicate FEEDBACK section and updated rating type to DECIMAL(2,1) -->

---

## Relationships

### 1. DEPARTMENTS ─< STAFF
- **Relationship Type:** One-to-Many
- **Description:** One department can have many staff members
- **Cardinality:** 1:N
- **Foreign Key:** staff.department_id references departments.department_id

### 2. ROOM_TYPES ─< ROOMS
- **Relationship Type:** One-to-Many
- **Description:** One room type can have many rooms
- **Cardinality:** 1:N
- **Foreign Key:** rooms.type_id references room_types.type_id

### 3. GUESTS ─< BOOKINGS
- **Relationship Type:** One-to-Many
- **Description:** One guest can make many bookings
- **Cardinality:** 1:N
- **Foreign Key:** bookings.guest_id references guests.guest_id

### 4. ROOMS ─< BOOKINGS
- **Relationship Type:** One-to-Many
- **Description:** One room can have many bookings (at different times)
- **Cardinality:** 1:N
- **Foreign Key:** bookings.room_id references rooms.room_id

### 5. BOOKINGS ─< PAYMENTS
- **Relationship Type:** One-to-Many
- **Description:** One booking can have multiple payments
- **Cardinality:** 1:N
- **Foreign Key:** payments.booking_id references bookings.booking_id

---

## Visual ER Diagram

```
┌─────────────────┐
│  DEPARTMENTS    │
├─────────────────┤
│ PK: department_id│
│    department_name│
│    description   │
└────────┬────────┘
         │
         │ 1:N (has)
         │
         ▼
┌─────────────────┐
│     STAFF       │
├─────────────────┤
│ PK: staff_id    │
│    first_name   │
│    last_name    │
│    email        │
│    phone        │
│ FK: department_id│
│    position     │
│    salary       │
│    hire_date    │
│    status       │
└─────────────────┘


┌─────────────────┐
│  ROOM_TYPES     │
├─────────────────┤
│ PK: type_id     │
│    type_name    │
│    description  │
│    base_price   │
│    capacity     │
└────────┬────────┘
         │
         │ 1:N (categorizes)
         │
         ▼
┌─────────────────┐
│     ROOMS       │
├─────────────────┤
│ PK: room_id     │
│    room_number  │
│ FK: type_id     │
│    floor        │
│    status       │
│    last_cleaned │
└────────┬────────┘
         │
         │ 1:N (booked_in)
         │
         ▼
┌─────────────────┐         ┌─────────────────┐
│     GUESTS      │         │    BOOKINGS     │
├─────────────────┤         ├─────────────────┤
│ PK: guest_id    │  1:N    │ PK: booking_id  │
│    first_name   │─────────│ FK: guest_id    │
│    last_name    │(makes)  │ FK: room_id     │
│    email        │         │    check_in_date│
│    phone        │         │    check_out_date│
│    address      │         │    actual_check_in│
│    city         │         │    actual_check_out│
│    country      │         │    num_adults   │
│    id_proof_type│         │    num_children │
│    id_proof_number │      │    booking_status│
│    registration_date │     │    total_amount │
└─────────────────┘         │    special_req  │
                            │    booking_date │
                            └────────┬────────┘
                                     │
                                     │ 1:N (paid_by)
                                     │
                                     ▼
                            ┌─────────────────┐
                            │    PAYMENTS     │
                            ├─────────────────┤
                            │ PK: payment_id  │
                            │ FK: booking_id  │
                            │    amount       │
                            │    payment_date │
                            │    payment_method│
                            │    payment_status│
                            │    transaction_id│
                            └─────────────────┘
                                     │
                                     │ 1:N (reviewed_by)
                                     ▼
                            ┌─────────────────┐
                            │    FEEDBACK     │
                            ├─────────────────┤
                            │ PK: feedback_id │
                            │ FK: booking_id  │
                            │    rating (2,1) │
                            │    comment      │
                            │    feedback_date│
                            └─────────────────┘
```

---

## Cardinality Summary

| Relationship | Parent Entity | Child Entity | Cardinality | Description |
|--------------|---------------|--------------|-------------|-------------|
| Works In | DEPARTMENTS | STAFF | 1:N | Each staff works in one department |
| Has Type | ROOM_TYPES | ROOMS | 1:N | Each room has one type |
| Makes | GUESTS | BOOKINGS | 1:N | Each guest can make multiple bookings |
| Books | ROOMS | BOOKINGS | 1:N | Each room can be booked multiple times |
| Pays For | BOOKINGS | PAYMENTS | 1:N | Each booking can have multiple payments |

---

## Business Rules

1. **Guest Registration:**
   - A guest must be registered before making a booking
   - Email must be unique for each guest
   - Phone number is mandatory

2. **Room Management:**
   - Each room must belong to exactly one room type
   - Room numbers must be unique
   - Room status affects availability for booking

3. **Booking Process:**
   - A booking requires both a guest and a room
   - Check-out date must be after check-in date
   - Multiple bookings allowed for same room (different dates)
   - Booking status tracks lifecycle: confirmed → checked-in → checked-out

4. **Payment Processing:**
   - Multiple payments allowed per booking (installments)
   - Total payments should equal booking total_amount
   - Payment methods are restricted to predefined options

5. **Staff Management:**
   - Staff must belong to a department
   - Email must be unique
   - Active/inactive status for employment tracking

---

## Database Normalization

### First Normal Form (1NF)
✓ All tables have atomic values
✓ No repeating groups
✓ Each column contains only one value

### Second Normal Form (2NF)
✓ All non-key attributes fully depend on primary key
✓ No partial dependencies exist

### Third Normal Form (3NF)
✓ No transitive dependencies
✓ All attributes depend only on the primary key

---

## Indexes for Performance

```sql
-- Frequently searched columns
CREATE INDEX idx_room_status ON rooms(status);
CREATE INDEX idx_booking_dates ON bookings(check_in_date, check_out_date);
CREATE INDEX idx_booking_status ON bookings(booking_status);
CREATE INDEX idx_guest_email ON guests(email);
CREATE INDEX idx_staff_department ON staff(department_id);
```

---

## Constraints Summary

### Primary Keys
- All tables have auto-incrementing integer primary keys

### Foreign Keys
- staff.department_id → departments.department_id
- rooms.type_id → room_types.type_id
- bookings.guest_id → guests.guest_id
- bookings.room_id → rooms.room_id
- payments.booking_id → bookings.booking_id

### Unique Constraints
- guests.email
- staff.email
- rooms.room_number

### Check Constraints (via ENUM)
- rooms.status: available, occupied, maintenance, reserved
- staff.status: active, inactive
- bookings.booking_status: confirmed, checked-in, checked-out, cancelled
- payments.payment_method: cash, credit_card, debit_card, upi, net_banking
- payments.payment_status: pending, completed, refunded

---

## ER Diagram Tool Notation

For drawing in tools like Draw.io, MySQL Workbench, or ERDPlus:

**Entities:** Rectangles  
**Attributes:** Ovals  
**Primary Keys:** Underlined  
**Foreign Keys:** Dashed underline  
**Relationships:** Diamonds  
**Cardinality:** 1, N, M notations on relationship lines
