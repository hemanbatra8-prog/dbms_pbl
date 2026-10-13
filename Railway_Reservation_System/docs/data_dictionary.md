# RELATIONAL DATA DICTIONARY
## Railway Ticket Reservation and Journey Management System
**Course:** Database Management Systems (B.Tech CSE)  
**Target RDBMS:** MySQL 8.x (InnoDB Transactional Engine) / SQLite Dev Fallback  
**Design Level:** Third Normal Form (3NF)

---

### Table 1: `stations`
*Description:* Defines physical railway passenger stations and terminal locations.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `station_id` | INT | PK | No | AUTO_INCREMENT | Unique surrogate primary key for the station |
| `station_code` | VARCHAR(10) | Unique | No | UNIQUE, INDEX | IRCTC alphabetic station code (e.g., 'NDLS', 'CNB') |
| `station_name` | VARCHAR(100) | None | No | None | Official station name (e.g., 'Kanpur Central') |
| `city` | VARCHAR(100) | None | No | None | Municipal city name |
| `state` | VARCHAR(100) | None | No | None | Indian State / Union Territory |

---

### Table 2: `routes`
*Description:* Represents fixed physical rail corridors connecting an origin and destination station.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `route_id` | INT | PK | No | AUTO_INCREMENT | Unique identifier for route |
| `route_code` | VARCHAR(30) | Unique | No | UNIQUE, INDEX | Alphanumeric route identifier (e.g., 'RT-NDLS-BSB') |
| `source_station_id` | INT | FK | No | REFERENCES stations(station_id) ON DELETE RESTRICT | Starting station of the route corridor |
| `destination_station_id` | INT | FK | No | REFERENCES stations(station_id) ON DELETE RESTRICT | Terminating station of the route corridor |
| `total_distance_km` | DECIMAL(7,2) | None | No | CHECK (total_distance_km > 0) | Cumulative track length in kilometers |

---

### Table 3: `train_stops`
*Description:* Stores the ordered sequence of intermediate station stops along a route.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `stop_id` | INT | PK | No | AUTO_INCREMENT | Unique stop surrogate key |
| `route_id` | INT | FK | No | REFERENCES routes(route_id) ON DELETE CASCADE | Associated railway route |
| `station_id` | INT | FK | No | REFERENCES stations(station_id) ON DELETE RESTRICT | Halting railway station |
| `stop_sequence` | INT | None | No | CHECK (stop_sequence > 0), UNIQUE(route_id, stop_sequence) | Sequential stop order (1, 2, 3...) |
| `distance_from_source_km`| DECIMAL(7,2) | None | No | CHECK (distance_from_source_km >= 0) | Track distance from route source station |
| `arrival_time` | TIME | None | Yes | NULL for first station | Scheduled train arrival time |
| `departure_time` | TIME | None | Yes | NULL for last station | Scheduled train departure time |

---

### Table 4: `trains`
*Description:* Master catalog defining static train locomotive definitions.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `train_id` | INT | PK | No | AUTO_INCREMENT | Unique primary key for train |
| `train_number` | VARCHAR(10) | Unique | No | UNIQUE, INDEX | 5-digit official train number (e.g., '22436') |
| `train_name` | VARCHAR(100) | None | No | None | Train designation (e.g., 'Vande Bharat Express') |
| `train_type` | VARCHAR(30) | None | No | None | Category (Rajdhani, Superfast, Shatabdi) |
| `route_id` | INT | FK | No | REFERENCES routes(route_id) ON DELETE RESTRICT | Operational route traversed |

---

### Table 5: `train_runs`
*Description:* Operational train run schedules decoupled from train definitions (3NF requirement).

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `run_id` | INT | PK | No | AUTO_INCREMENT | Unique train run operational key |
| `train_id` | INT | FK | No | REFERENCES trains(train_id) ON DELETE CASCADE | Train operating on this date |
| `run_date` | DATE | None | No | INDEX, UNIQUE(train_id, run_date) | Calendar date of scheduled departure |
| `status` | VARCHAR(20) | None | No | DEFAULT 'SCHEDULED' | Operational status (SCHEDULED, CANCELLED) |

---

### Table 6: `coaches`
*Description:* Rolling stock carriages attached to a train.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `coach_id` | INT | PK | No | AUTO_INCREMENT | Coach primary key |
| `train_id` | INT | FK | No | REFERENCES trains(train_id) ON DELETE CASCADE | Train carrying this coach |
| `coach_code` | VARCHAR(10) | None | No | UNIQUE(train_id, coach_code) | Carriage code (e.g., 'C1', 'B1', 'A1', 'H1') |
| `travel_class` | VARCHAR(10) | None | No | INDEX | Travel class designation (1A, 2A, 3A, CC, SL) |
| `total_seats` | INT | None | No | DEFAULT 72, CHECK (total_seats > 0) | Physical seating capacity of coach |

---

### Table 7: `seats`
*Description:* Individual seating units inside coaches.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `seat_id` | INT | PK | No | AUTO_INCREMENT | Unique physical seat identifier |
| `coach_id` | INT | FK | No | REFERENCES coaches(coach_id) ON DELETE CASCADE | Parent coach |
| `seat_number` | INT | None | No | CHECK (seat_number > 0), UNIQUE(coach_id, seat_number)| Number label within coach (1 to 72) |
| `berth_type` | VARCHAR(15) | None | No | None | Berth location (LOWER, UPPER, SIDE LOWER, WINDOW) |

---

### Table 8: `passengers`
*Description:* Registered customer traveler profiles decoupled from individual reservations (3NF requirement).

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `passenger_id` | INT | PK | No | AUTO_INCREMENT | Unique passenger surrogate key |
| `full_name` | VARCHAR(100) | None | No | None | Full legal passenger name |
| `gender` | VARCHAR(10) | None | No | None | 'MALE', 'FEMALE', 'OTHER' |
| `age` | INT | None | No | CHECK (age > 0 AND age < 120) | Age in years |
| `email` | VARCHAR(120) | None | No | INDEX | Verified contact email |
| `phone` | VARCHAR(20) | None | No | None | 10-digit mobile contact number |
| `id_card_type` | VARCHAR(20) | None | No | None | Government ID type (AADHAAR, PASSPORT, PAN) |
| `id_card_number` | VARCHAR(50) | None | No | None | Document verification number |

---

### Table 9: `fare_rules`
*Description:* Deterministic tariff and pricing formula table.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `fare_id` | INT | PK | No | AUTO_INCREMENT | Fare rule primary key |
| `train_type` | VARCHAR(30) | None | No | UNIQUE(train_type, travel_class) | Category (Rajdhani, Superfast, Shatabdi) |
| `travel_class` | VARCHAR(10) | None | No | None | Class code (1A, 2A, 3A, CC, SL) |
| `base_fare` | DECIMAL(10,2) | None | No | CHECK (base_fare >= 0) | Minimum initial boarding charge |
| `rate_per_km` | DECIMAL(6,2) | None | No | CHECK (rate_per_km >= 0) | Variable distance rate per kilometer |
| `reservation_fee` | DECIMAL(6,2)| None | No | DEFAULT 40.00, CHECK (reservation_fee >= 0)| Administrative surcharge |

---

### Table 10: `bookings`
*Description:* Main transactional booking record representing a journey reservation.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `booking_id` | INT | PK | No | AUTO_INCREMENT | Booking surrogate primary key |
| `pnr_number` | VARCHAR(12) | Unique | No | UNIQUE, INDEX | 10-digit Passenger Name Record reference |
| `run_id` | INT | FK | No | REFERENCES train_runs(run_id) ON DELETE RESTRICT | Target dated train run |
| `passenger_id` | INT | FK | No | REFERENCES passengers(passenger_id) ON DELETE RESTRICT | Traveling passenger |
| `origin_station_id` | INT | FK | No | REFERENCES stations(station_id) ON DELETE RESTRICT | Boarding station |
| `destination_station_id`| INT | FK | No | REFERENCES stations(station_id) ON DELETE RESTRICT | Deboarding station |
| `origin_stop_seq` | INT | None | No | None | Boarding stop sequence number |
| `destination_stop_seq` | INT | None | No | CHECK (destination_stop_seq > origin_stop_seq)| Deboarding stop sequence number |
| `travel_class` | VARCHAR(10) | None | No | None | Chosen class (1A, 2A, 3A, CC, SL) |
| `booking_status` | VARCHAR(20) | None | No | DEFAULT 'CONFIRMED', INDEX | 'CONFIRMED', 'WAITLISTED', 'CANCELLED' |
| `total_fare` | DECIMAL(10,2) | None | No | CHECK (total_fare >= 0) | Total calculated ticket price |
| `booked_at` | DATETIME | None | No | DEFAULT CURRENT_TIMESTAMP | Timestamp of reservation |

---

### Table 11: `journey_segments`
*Description:* Core segment-wise seat allocation over half-open station stop intervals $[start\_stop\_seq, end\_stop\_seq)$.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `segment_id` | INT | PK | No | AUTO_INCREMENT | Segment allocation key |
| `booking_id` | INT | FK | No | REFERENCES bookings(booking_id) ON DELETE CASCADE | Associated booking |
| `seat_id` | INT | FK | No | REFERENCES seats(seat_id) ON DELETE RESTRICT | Specific allocated seat |
| `run_id` | INT | FK | No | REFERENCES train_runs(run_id) ON DELETE CASCADE | Operational run |
| `start_stop_seq` | INT | None | No | None | Interval beginning stop sequence |
| `end_stop_seq` | INT | None | No | CHECK (end_stop_seq > start_stop_seq) | Interval termination stop sequence |
| `allocation_status`| VARCHAR(20) | None | No | DEFAULT 'ACTIVE', INDEX(run_id, seat_id, allocation_status)| 'ACTIVE' or 'CANCELLED' |

---

### Table 12: `waitlists`
*Description:* Sequenced priority FIFO queue for unconfirmed booking requests.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `waitlist_id` | INT | PK | No | AUTO_INCREMENT | Waitlist record key |
| `booking_id` | INT | FK | No | REFERENCES bookings(booking_id) ON DELETE CASCADE | Waitlisted booking |
| `run_id` | INT | FK | No | REFERENCES train_runs(run_id) ON DELETE CASCADE | Train run |
| `travel_class` | VARCHAR(10) | None | No | None | Requested travel class |
| `origin_stop_seq` | INT | None | No | None | Requested boarding sequence |
| `destination_stop_seq`| INT | None | No | CHECK (destination_stop_seq > origin_stop_seq)| Requested deboarding sequence |
| `position` | INT | None | No | CHECK (position > 0), INDEX(run_id, travel_class, position)| Queue priority index (1, 2, 3...) |
| `waitlist_status` | VARCHAR(20) | None | No | DEFAULT 'WAITING', INDEX | 'WAITING', 'PROMOTED', 'CANCELLED' |
| `created_at` | DATETIME | None | No | DEFAULT CURRENT_TIMESTAMP | Queue insertion timestamp |

---

### Table 13: `payments`
*Description:* Financial payment ledger recording simulated transactions.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `payment_id` | INT | PK | No | AUTO_INCREMENT | Payment transaction key |
| `booking_id` | INT | FK | No | REFERENCES bookings(booking_id) ON DELETE CASCADE | Paid booking |
| `amount` | DECIMAL(10,2) | None | No | CHECK (amount >= 0) | Exact financial amount |
| `payment_method` | VARCHAR(30) | None | No | DEFAULT 'SIMULATED_UPI' | UPI, CARD, NETBANKING |
| `transaction_reference`| VARCHAR(60) | Unique | No | UNIQUE, INDEX | Unique audit transaction string |
| `payment_status` | VARCHAR(20) | None | No | DEFAULT 'COMPLETED' | 'COMPLETED', 'REFUNDED', 'FAILED' |
| `paid_at` | DATETIME | None | No | DEFAULT CURRENT_TIMESTAMP | Payment settlement timestamp |

---

### Table 14: `cancellations`
*Description:* Historical cancellation ledger recording fee retention and refund disbursements.

| Column Name | Data Type | PK/FK | Nullable | Constraints & Defaults | Description |
|---|---|---|---|---|---|
| `cancellation_id` | INT | PK | No | AUTO_INCREMENT | Cancellation record key |
| `booking_id` | INT | Unique | No | REFERENCES bookings(booking_id) ON DELETE RESTRICT | Cancelled booking reference |
| `cancellation_reason` | VARCHAR(255)| None | No | None | Stated passenger reason |
| `cancellation_fee` | DECIMAL(10,2)| None | No | DEFAULT 0.00, CHECK (cancellation_fee >= 0)| Retained administrative deduction |
| `refund_amount` | DECIMAL(10,2)| None | No | CHECK (refund_amount >= 0) | Exact refund processed |
| `refund_status` | VARCHAR(20) | None | No | DEFAULT 'PROCESSED' | Settlement status |
| `cancelled_at` | DATETIME | None | No | DEFAULT CURRENT_TIMESTAMP | Cancellation timestamp |
