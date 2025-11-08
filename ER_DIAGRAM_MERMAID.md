# Hotel Management System - ER Diagram (Mermaid)

This diagram can be rendered in GitHub, VS Code with Mermaid extension, or online at https://mermaid.live/

## Entity Relationship Diagram

```mermaid
erDiagram
    DEPARTMENTS ||--o{ STAFF : "employs"
    ROOM_TYPES ||--o{ ROOMS : "categorizes"
    GUESTS ||--o{ BOOKINGS : "makes"
    ROOMS ||--o{ BOOKINGS : "booked_in"
    BOOKINGS ||--o{ PAYMENTS : "paid_by"
    BOOKINGS ||--o{ FEEDBACK : "reviewed_by"

    DEPARTMENTS {
        int department_id PK
        varchar department_name
        text description
    }

    STAFF {
        int staff_id PK
        varchar first_name
        varchar last_name
        varchar email UK "UNIQUE"
        varchar phone
        int department_id FK
        varchar position
        decimal salary
        date hire_date
        enum status "active/inactive"
    }

    ROOM_TYPES {
        int type_id PK
        varchar type_name
        text description
        decimal base_price
        int capacity
    }

    ROOMS {
        int room_id PK
        varchar room_number UK "UNIQUE"
        int type_id FK
        int floor
        enum status "available/occupied/maintenance/reserved"
        datetime last_cleaned
    }

    GUESTS {
        int guest_id PK
        varchar first_name
        varchar last_name
        varchar email UK "UNIQUE"
        varchar phone
        text address
        varchar city
        varchar country
        varchar id_proof_type
        varchar id_proof_number
        datetime registration_date
    }

    BOOKINGS {
        int booking_id PK
        int guest_id FK
        int room_id FK
        date check_in_date
        date check_out_date
        datetime actual_check_in
        datetime actual_check_out
        int num_adults
        int num_children
        enum booking_status "confirmed/checked-in/checked-out/cancelled"
        decimal total_amount
        text special_requests
        datetime booking_date
    }

    PAYMENTS {
        int payment_id PK
        int booking_id FK
        decimal amount
        datetime payment_date
        enum payment_method "cash/credit_card/debit_card/upi/net_banking"
        enum payment_status "pending/completed/refunded"
        varchar transaction_id
    }

    FEEDBACK {
        int feedback_id PK
        int booking_id FK
        decimal rating "DECIMAL(2,1) - supports 0.5 steps (1.0-5.0)"
        text comment
        datetime feedback_date
    }
```

## How to Render

### Option 1: GitHub
Just view this file on GitHub - Mermaid is automatically rendered.

### Option 2: VS Code
1. Install "Markdown Preview Mermaid Support" extension
2. Open this file and press `Ctrl+Shift+V` (preview)

### Option 3: Online
1. Copy the mermaid code block above
2. Go to https://mermaid.live/
3. Paste and export as PNG/SVG

### Option 4: CLI (requires Node.js)
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i ER_DIAGRAM_MERMAID.md -o ER_DIAGRAM.png
```

## Relationship Summary

| Relationship | Parent → Child | Type | Description |
|--------------|----------------|------|-------------|
| employs | DEPARTMENTS → STAFF | 1:N | Each department has multiple staff |
| categorizes | ROOM_TYPES → ROOMS | 1:N | Each room type has multiple rooms |
| makes | GUESTS → BOOKINGS | 1:N | Each guest can make multiple bookings |
| booked_in | ROOMS → BOOKINGS | 1:N | Each room can have multiple bookings |
| paid_by | BOOKINGS → PAYMENTS | 1:N | Each booking can have multiple payments |
| reviewed_by | BOOKINGS → FEEDBACK | 1:N | Each booking can have multiple feedback entries |

## Key Features
- ✅ All 8 entities with complete attributes
- ✅ Primary keys (PK) and Foreign keys (FK) marked
- ✅ Unique constraints (UK) indicated
- ✅ ENUM types documented with values
- ✅ DECIMAL(2,1) rating for half-star support (3.5, 4.5, etc.)
- ✅ All relationships with cardinality (1:N)
