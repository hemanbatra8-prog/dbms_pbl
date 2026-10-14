"""
Structured Project Data, Tables, and Content for Woxsen University DBMS PBL Report.
Project: Railway Ticket Reservation and Journey Management System Using Relational Database Management Systems
Student: Heman (25WU0102097) | Section: AIML Rhinos | Faculty Mentor: Prof. Sahithi
"""

PROJECT_TITLE = "RAILWAY TICKET RESERVATION AND JOURNEY MANAGEMENT SYSTEM USING RELATIONAL DATABASE MANAGEMENT SYSTEMS"

STUDENT_DETAILS = {
    "name": "Heman",
    "roll_no": "25WU0102097",
    "program": "B.Tech Computer Science & Engineering (Artificial Intelligence & Machine Learning)",
    "section": "AIML Rhinos",
    "faculty": "Prof. Sahithi",
    "institution": "School of Technology, Woxsen University, Hyderabad",
    "date": "October 14, 2026",
    "year": "2026 – 27",
    "mobile": "+91 98765 43210",
    "email": "heman.25wu0102097@woxsen.edu.in",
    "place": "Hyderabad"
}

# -------------------------------------------------------------------------
# TABLE OF CONTENTS
# -------------------------------------------------------------------------
TOC_DATA = [
    ("Abstract", "5"),
    ("LIST OF TABLES", "6"),
    ("LIST OF FIGURES", "7"),
    ("LIST OF ACRONYMS", "8"),
    ("1. PROBLEM STATEMENT, SOLUTION STRATEGY AND ER DIAGRAM", "9"),
    ("   1.1 Problem Statement", "9"),
    ("   1.2 Objectives", "10"),
    ("   1.3 Scope and Assumptions", "10"),
    ("   1.4 Proposed Solution Strategy", "11"),
    ("   1.5 Functional Requirements", "13"),
    ("   1.6 Entity-Relationship Diagram (ERD)", "14"),
    ("   1.7 Entity and Relationship Summary", "15"),
    ("2. LOGICAL DATABASE DESIGN", "17"),
    ("   2.1 Relational Schema", "17"),
    ("   2.2 Keys and Integrity Constraints", "19"),
    ("   2.3 Functional Dependencies", "21"),
    ("   2.4 Normalization up to Third Normal Form (3NF)", "23"),
    ("   2.5 Data Dictionary", "26"),
    ("   2.6 Implementation of Logical Design: DDL and Sample Data", "29"),
    ("3. APPLICATION DEVELOPMENT USING LOGICAL DATABASE DESIGN", "33"),
    ("   3.1 Application Overview", "33"),
    ("   3.2 Development Environment and Database Connectivity", "34"),
    ("   3.3 Application Modules and Database Mapping", "35"),
    ("   3.4 CRUD Operations", "37"),
    ("   3.5 Business Rules, Validation and Error Handling", "39"),
    ("   3.6 Reports and Database Operations", "41"),
    ("   3.7 Application Screens", "44"),
    ("   3.8 Testing and Results", "48"),
    ("4. CONCLUSION", "51"),
    ("   4.1 Limitations and Future Enhancements", "51"),
    ("5. REFERENCES", "53"),
    ("6. APPENDICES", "54"),
    ("   Appendix A — Complete Database Script", "54"),
    ("   Appendix B — Application Source Code", "55"),
    ("   Appendix C — Additional Test Data and Outputs", "56"),
]

# -------------------------------------------------------------------------
# LIST OF TABLES
# -------------------------------------------------------------------------
TABLES_LIST = [
    ("Table 1", "Scope and Assumptions", "10"),
    ("Table 2", "Proposed Solution Strategy", "12"),
    ("Table 3", "Functional Requirements", "13"),
    ("Table 4", "Entity and Relationship Summary", "15"),
    ("Table 5", "Relational Schema", "17"),
    ("Table 6", "Keys and Integrity Constraints", "19"),
    ("Table 7", "Normalization Status up to 3NF", "23"),
    ("Table 8", "Data Dictionary", "26"),
    ("Table 9", "Database Implementation Environment", "29"),
    ("Table 10", "Application Development Environment", "34"),
    ("Table 11", "Application Module-to-Database Mapping", "36"),
    ("Table 12", "CRUD Operations", "37"),
    ("Table 13", "Business Rules, Validation and Error Handling", "39"),
    ("Table 14", "Reports and Database Operations", "42"),
    ("Table 15", "Test Cases", "49"),
]

# -------------------------------------------------------------------------
# LIST OF FIGURES
# -------------------------------------------------------------------------
FIGURES_LIST = [
    ("Figure 1", "Entity-Relationship Diagram of the Proposed System", "14"),
    ("Figure 2", "Executive Analytics and Key Performance Indicator (KPI) Dashboard", "44"),
    ("Figure 3", "Multi-Hop Train Search and Segment Seat Inventory Results", "45"),
    ("Figure 4", "Confirmed Electronic Reservation Slip (ERS Ticket Confirmation)", "46"),
    ("Figure 5", "Live Waitlist Queue and Real-Time Position Tracking", "46"),
    ("Figure 6", "Executive SQL Analytical Reports Console", "47"),
    ("Figure 7", "Relational Database Schema Explorer and Administrative Inventory Control", "47"),
]

# -------------------------------------------------------------------------
# LIST OF ACRONYMS
# -------------------------------------------------------------------------
ACRONYMS_DATA = [
    ("ACID", "Atomicity, Consistency, Isolation, and Durability"),
    ("AIML", "Artificial Intelligence and Machine Learning"),
    ("API", "Application Programming Interface"),
    ("BCNF", "Boyce-Codd Normal Form"),
    ("CRUD", "Create, Read, Update, and Delete"),
    ("DDL", "Data Definition Language"),
    ("DML", "Data Manipulation Language"),
    ("ERD", "Entity-Relationship Diagram"),
    ("ERS", "Electronic Reservation Slip"),
    ("FIFO", "First-In, First-Out"),
    ("FK", "Foreign Key"),
    ("HTML", "Hypertext Markup Language"),
    ("IDE", "Integrated Development Environment"),
    ("IRCTC", "Indian Railway Catering and Tourism Corporation"),
    ("KPI", "Key Performance Indicator"),
    ("ORM", "Object-Relational Mapping"),
    ("PBL", "Project-Based Learning"),
    ("PK", "Primary Key"),
    ("PNR", "Passenger Name Record"),
    ("RDBMS", "Relational Database Management System"),
    ("SQL", "Structured Query Language"),
    ("1NF", "First Normal Form"),
    ("2NF", "Second Normal Form"),
    ("3NF", "Third Normal Form"),
    ("UI", "User Interface"),
    ("UPI", "Unified Payments Interface"),
]

# -------------------------------------------------------------------------
# ABSTRACT & KEYWORDS
# -------------------------------------------------------------------------
ABSTRACT_TEXT = (
    "This project presents the design, relational formalization, full-stack implementation, and automated verification "
    "of the Railway Ticket Reservation and Journey Management System, an academic software solution engineered to resolve "
    "the multi-hop inventory allocation dilemma in passenger rail transport. Unlike point-to-point airline reservation models "
    "where seats are locked for entire flights, passenger railway networks traverse ordered station corridors requiring "
    "dynamic segment-wise berth reuse. To address the risk of catastrophic double-booking across overlapping sub-journeys, "
    "this system implements a mathematically formalized half-open interval model [start_stop_seq, end_stop_seq) that strictly "
    "evaluates interval overlap constraints while enabling non-conflicting seat reuse. The underlying relational database is "
    "modeled across 14 decoupled relations strictly normalized to Third Normal Form (3NF) on MySQL 8.x InnoDB, enforcing referential "
    "integrity, domain constraints, and pessimistic row locking (SELECT ... FOR UPDATE) to guarantee ACID transactional safety "
    "during concurrent checkouts. Developed using Python 3.9, Flask, SQLAlchemy, HTML5, and Bootstrap 5, the application delivers "
    "end-to-end journey planning, electronic ticket generation, FIFO waitlist promotion, and twelve analytical SQL reports, "
    "verified through sixteen comprehensive automated pytest unit and integration test suites."
)

KEYWORDS_TEXT = (
    "Relational Database, Entity-Relationship Modeling, Third Normal Form (3NF), "
    "Multi-Hop Inventory, Segment Interval Allocation, ACID Concurrency, Python Flask, MySQL InnoDB"
)

# -------------------------------------------------------------------------
# TABLE 1: SCOPE AND ASSUMPTIONS
# -------------------------------------------------------------------------
TABLE_1_HEADERS = ["Item", "Description"]
TABLE_1_ROWS = [
    [
        "In Scope",
        "1. Complete relational schema modeling 14 distinct relations in Third Normal Form (3NF).\n"
        "2. Multi-hop segment-wise seat allocation over half-open station intervals [s, e).\n"
        "3. Pessimistic row-level locking (SELECT ... FOR UPDATE) to prevent race-condition overbooking.\n"
        "4. Automated FIFO waitlist queue insertion and immediate promotion upon ticket cancellation.\n"
        "5. Cancellation and refund processing enforcing 20% penalty deductions.\n"
        "6. Analytical SQL reporting engine executing 12 benchmark aggregation queries.\n"
        "7. Full-stack responsive web prototype built with Python Flask and SQLAlchemy."
    ],
    [
        "Out of Scope / Exclusions",
        "1. Real-time physical locomotive telemetry and GPS sensor integration.\n"
        "2. Dynamic locomotive crew rostering and maintenance bay scheduling.\n"
        "3. Dynamic pricing algorithms responding to external flight/bus market fluctuations.\n"
        "4. Live commercial banking gateway settlement (handled via simulated deterministic UPI payment engine)."
    ],
    [
        "Assumptions",
        "1. Stations along a route possess strictly monotonically increasing sequence IDs (dest_seq > orig_seq).\n"
        "2. Coach seat allocations follow standard Indian Railways layout conventions (LB, MB, UB, SL, SU).\n"
        "3. Train schedules operate as distinct, dated train run instances decoupled from catalog definitions.\n"
        "4. Platform track allocation and mechanical signaling are managed by external signaling systems."
    ]
]

# -------------------------------------------------------------------------
# TABLE 2: PROPOSED SOLUTION STRATEGY
# -------------------------------------------------------------------------
TABLE_2_HEADERS = ["Solution Element", "Project-Specific Description"]
TABLE_2_ROWS = [
    [
        "Primary Users / Roles",
        "1. Passenger: Search train availability, reserve berths, view PNR status, manage waitlists, and process cancellations.\n"
        "2. Station Master / Ticket Collector: View passenger booking manifests, inspect train schedules, and check coach charts.\n"
        "3. Operations Administrator: Manage train inventory, configure fare rules, and inspect analytical database reports."
    ],
    [
        "Major Application Modules",
        "1. Train Search & Inventory Discovery Module.\n"
        "2. Booking & Interval-Overlap Seat Allocation Service.\n"
        "3. Electronic Reservation Slip (ERS) & Ticket Generation Engine.\n"
        "4. Automated Waitlist Queue & Dynamic Promotion Processor.\n"
        "5. Cancellation, Refund & Financial Audit Module.\n"
        "6. Analytical SQL Query & KPI Reporting Console."
    ],
    [
        "Proposed Workflow",
        "Passenger searches trains by origin, destination, and date -> System validates station sequences -> "
        "System executes segment-wise non-overlap check across [s, e) -> Passenger submits passenger details -> "
        "Database initiates transaction with SELECT FOR UPDATE -> Confirmed PNR is generated with segment locks -> "
        "In case of full occupancy, passenger is assigned to FIFO waitlist -> Upon ticket cancellation, segment is freed "
        "and waitlist candidate is promoted atomically."
    ],
    [
        "Key Business Rules",
        "1. Interval Overlap Constraint: Two bookings conflict if and only if (s_new < e_exist) AND (e_new > s_exist).\n"
        "2. Waitlist FIFO Ordering: Earliest booked waitlist passenger receives immediate promotion when matching segment is freed.\n"
        "3. Cancellation Penalty: 20% flat deduction applied; 80% refunded to passenger payment record.\n"
        "4. Transaction Boundaries: Seat allocation, payment record, and PNR creation must commit atomically."
    ],
    [
        "Expected Outputs",
        "1. Real-time tabular train search results displaying class-wise berth availability.\n"
        "2. Formatted Electronic Reservation Slip (ERS) ticket with 10-digit PNR and passenger details.\n"
        "3. Dynamic waitlist queue position status.\n"
        "4. Executive analytical KPI reports with revenue, load factor, and passenger metrics."
    ]
]

# -------------------------------------------------------------------------
# TABLE 3: FUNCTIONAL REQUIREMENTS
# -------------------------------------------------------------------------
TABLE_3_HEADERS = ["Req. ID", "Functional Requirement", "Remarks / Priority"]
TABLE_3_ROWS = [
    ["FR-01", "Multi-Station Train Search: System shall accept source station, destination station, and travel date, and return all trains traversing that route where dest_seq > orig_seq.", "High / Core"],
    ["FR-02", "Segment-Wise Half-Open Interval Seat Calculation: System shall calculate remaining seat inventory by evaluating interval overlaps against active bookings on that specific dated run.", "High / Core"],
    ["FR-03", "Concurrency-Safe Ticket Booking: System shall create passenger, booking, journey segment, and payment records inside a serialized transaction using pessimistic row locking.", "High / Core"],
    ["FR-04", "Automated Waitlist Queuing: When seat inventory is zero, system shall allow passenger to enter a FIFO waitlist with an assigned queue position.", "High / Core"],
    ["FR-05", "Booking Cancellation and Automated Waitlist Promotion: Upon cancellation, system shall mark allocation CANCELLED, compute refund, and atomically promote next eligible waitlist passenger.", "High / Core"],
    ["FR-06", "Electronic Reservation Slip (ERS) Retrieval: System shall render printable booking slips by querying PNR number, displaying coach, seat, fare, and passenger details.", "Medium / Operational"],
    ["FR-07", "SQL Analytical Reporting: System shall execute 12 benchmark SQL reports covering revenue, occupancy, route demand, and passenger demographics.", "Medium / Analytics"],
    ["FR-08", "Admin Inventory & Schema Management: Administrators shall be able to inspect database table row counts, view coach configurations, and manage train schedules.", "Medium / Administrative"]
]

# -------------------------------------------------------------------------
# TABLE 4: ENTITY AND RELATIONSHIP SUMMARY
# -------------------------------------------------------------------------
TABLE_4_HEADERS = ["Entity / Relationship", "Major Attributes / Cardinality", "Purpose / Rule"]
TABLE_4_ROWS = [
    ["STATIONS", "station_id (PK), station_code, station_name, city, state", "Defines physical railway stations. station_code is unique."],
    ["ROUTES", "route_id (PK), route_code, source_station_id (FK), dest_station_id (FK), total_dist_km", "Defines operational railway corridors between terminal stations."],
    ["TRAIN_STOPS", "stop_id (PK), route_id (FK), station_id (FK), stop_sequence, distance_km, arr/dep time", "Ordered sequence of station halts. Unique on (route_id, stop_sequence)."],
    ["TRAINS", "train_id (PK), train_number, train_name, train_type, route_id (FK)", "Master train locomotive catalog. train_number is unique."],
    ["TRAIN_RUNS", "run_id (PK), train_id (FK), run_date, status", "Dated physical train operation instances decoupled from train catalog."],
    ["COACHES", "coach_id (PK), train_id (FK), coach_code, travel_class, total_seats", "Rake composition. Unique on (train_id, coach_code)."],
    ["SEATS", "seat_id (PK), coach_id (FK), seat_number, berth_type", "Individual berth instances. Unique on (coach_id, seat_number)."],
    ["PASSENGERS", "passenger_id (PK), full_name, gender, age, email, phone, id_card_type/no", "Customer master records. Age constrained to 1 <= age <= 120."],
    ["FARE_RULES", "fare_id (PK), train_type, travel_class, base_fare, rate_per_km, res_fee", "Tariff matrix. Unique on (train_type, travel_class)."],
    ["BOOKINGS", "booking_id (PK), pnr_number, run_id (FK), passenger_id (FK), orig/dest station, total_fare", "Header booking record. pnr_number is unique."],
    ["JOURNEY_SEGMENTS", "segment_id (PK), booking_id (FK), seat_id (FK), run_id (FK), start/end_seq, status", "Segment berth locks over [start_seq, end_seq). Evaluates overlap."],
    ["WAITLISTS", "waitlist_id (PK), booking_id (FK), run_id (FK), travel_class, position, status", "FIFO waiting queue for passengers booked on fully occupied segments."],
    ["PAYMENTS", "payment_id (PK), booking_id (FK), amount, txn_ref, status, paid_at", "Financial transaction log. txn_ref is unique."],
    ["CANCELLATIONS", "cancellation_id (PK), booking_id (FK), fee, refund_amount, status, cancelled_at", "Audit log of cancellations with 20% penalty calculation."],
    ["TRAIN -> COACHES -> SEATS", "1 : M (Train to Coach), 1 : M (Coach to Seat)", "Physical train composition hierarchy."],
    ["BOOKING -> SEGMENTS", "1 : M (Booking to Journey Segments)", "One booking reserves segments across traversed stations."],
    ["BOOKING -> PAYMENT / CANCEL", "1 : 1 (Booking to Payment), 1 : 0..1 (Booking to Cancellation)", "Financial transaction relationships."]
]

# -------------------------------------------------------------------------
# TABLE 5: RELATIONAL SCHEMA
# -------------------------------------------------------------------------
TABLE_5_HEADERS = ["S.No.", "Table Name", "Purpose"]
TABLE_5_ROWS = [
    ["1", "stations", "Stores railway stations with unique station codes, names, cities, and states."],
    ["2", "routes", "Defines geographical corridors connecting origin and destination terminal stations."],
    ["3", "train_stops", "Captures ordered stop sequences, inter-station distances, and timetable schedules."],
    ["4", "trains", "Master catalog for train entities, train numbers, and assigned route corridors."],
    ["5", "train_runs", "Decoupled operational calendar tracking specific dated train journeys."],
    ["6", "coaches", "Defines rake compositions, coach types, travel classes, and seating capacities."],
    ["7", "seats", "Catalog of individual physical berths and assigned berth types (LB, MB, UB, etc.)."],
    ["8", "passengers", "Master registry of passenger demographic and verified identity credential data."],
    ["9", "fare_rules", "Distance and class-based tariff structures for automated ticket fare computation."],
    ["10", "bookings", "Master reservation entity storing generated 10-digit PNRs and itinerary headers."],
    ["11", "journey_segments", "Granular physical berth interval locks allocated over half-open station intervals."],
    ["12", "waitlists", "Queue entity tracking overflow passenger booking requests in strict FIFO order."],
    ["13", "payments", "Financial transaction audit ledger recording transaction references and amounts."],
    ["14", "cancellations", "Cancellation ledger enforcing 20% fee policies and recording refund amounts."]
]

# -------------------------------------------------------------------------
# TABLE 6: KEYS AND INTEGRITY CONSTRAINTS
# -------------------------------------------------------------------------
TABLE_6_HEADERS = ["Table Name", "Key / Constraint", "Attribute(s)", "Business Rule Enforced"]
TABLE_6_ROWS = [
    ["stations", "Primary Key", "station_id", "Surrogate primary key ensuring entity uniqueness."],
    ["stations", "Unique Key", "station_code", "Prevents duplicate station abbreviations (e.g., 'NDLS')."],
    ["routes", "Foreign Key", "source_station_id", "Enforces valid origin station reference on DELETE RESTRICT."],
    ["routes", "Foreign Key", "destination_station_id", "Enforces valid destination station reference on DELETE RESTRICT."],
    ["routes", "Check Constraint", "total_distance_km", "Ensures track distance is strictly positive (> 0)."],
    ["train_stops", "Unique Key", "(route_id, stop_sequence)", "Guarantees stop sequence uniqueness along a route corridor."],
    ["train_stops", "Check Constraint", "stop_sequence", "Guarantees sequence is strictly positive (> 0)."],
    ["trains", "Unique Key", "train_number", "Enforces unique 5-digit locomotive identifier."],
    ["train_runs", "Unique Key", "(train_id, run_date)", "Prevents creating duplicate operational runs for the same train on the same day."],
    ["coaches", "Unique Key", "(train_id, coach_code)", "Prevents duplicate coach codes within the same train rake."],
    ["seats", "Unique Key", "(coach_id, seat_number)", "Guarantees berth number uniqueness within a specific coach."],
    ["passengers", "Check Constraint", "age", "Validates human age domain (age > 0 AND age < 120)."],
    ["bookings", "Unique Key", "pnr_number", "Guarantees global uniqueness of 10-digit PNR strings."],
    ["bookings", "Check Constraint", "dest_stop_seq > orig_stop_seq", "Enforces forward-only travel sequence order."],
    ["journey_segments", "Foreign Key", "booking_id, seat_id, run_id", "Enforces referential integrity on allocation locks."],
    ["journey_segments", "Check Constraint", "end_stop_seq > start_stop_seq", "Validates half-open interval ordering."],
    ["waitlists", "Check Constraint", "position > 0", "Enforces positive FIFO queue position numbers."],
    ["payments", "Unique Key", "transaction_reference", "Prevents financial transaction re-play and duplicate billing."],
    ["cancellations", "Unique Key", "booking_id", "Guarantees a ticket can only be cancelled once (1:1 constraint)."]
]

# -------------------------------------------------------------------------
# TABLE 7: NORMALIZATION STATUS UP TO 3NF
# -------------------------------------------------------------------------
TABLE_7_HEADERS = ["Relation Name", "1NF", "2NF", "3NF", "BCNF", "Remarks / Decomposition"]
TABLE_7_ROWS = [
    ["stations", "Yes", "Yes", "Yes", "Yes", "All attributes atomic; single-attribute primary key station_id."],
    ["routes", "Yes", "Yes", "Yes", "Yes", "No partial or transitive dependencies. Endpoints separated from stops."],
    ["train_stops", "Yes", "Yes", "Yes", "Yes", "Stop sequence depends on composite key (route_id, stop_sequence)."],
    ["trains", "Yes", "Yes", "Yes", "Yes", "Route foreign key isolated from physical train attributes."],
    ["train_runs", "Yes", "Yes", "Yes", "Yes", "Dated runs isolated from static train definitions to eliminate redundancy."],
    ["coaches", "Yes", "Yes", "Yes", "Yes", "Coach definitions decoupled from seat lists; total_seats is atomic."],
    ["seats", "Yes", "Yes", "Yes", "Yes", "Berth type depends entirely on (coach_id, seat_number)."],
    ["passengers", "Yes", "Yes", "Yes", "Yes", "Customer attributes separated from reservation instances."],
    ["fare_rules", "Yes", "Yes", "Yes", "Yes", "Tariff rates isolated from individual passenger booking tickets."],
    ["bookings", "Yes", "Yes", "Yes", "Yes", "Station IDs and stop sequences depend on booking_id. 3NF preserved."],
    ["journey_segments", "Yes", "Yes", "Yes", "Yes", "Berth allocation intervals decoupled from booking headers."],
    ["waitlists", "Yes", "Yes", "Yes", "Yes", "Queue position isolated in separate entity to prevent booking table nulls."],
    ["payments", "Yes", "Yes", "Yes", "Yes", "Financial ledger decoupled from reservation headers."],
    ["cancellations", "Yes", "Yes", "Yes", "Yes", "1:1 extension relation; null attributes avoided in bookings table."]
]

# -------------------------------------------------------------------------
# TABLE 8: DATA DICTIONARY
# -------------------------------------------------------------------------
TABLE_8_HEADERS = ["Table", "Attribute", "Data Type", "Key / Constraint", "Description"]
TABLE_8_ROWS = [
    # 1. stations
    ["stations", "station_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for station entity."],
    ["stations", "station_code", "VARCHAR(10)", "UNIQUE, NOT NULL", "Official IRCTC alphabetic station abbreviation code."],
    ["stations", "station_name", "VARCHAR(100)", "NOT NULL", "Official full station designation."],
    ["stations", "city", "VARCHAR(100)", "NOT NULL", "Municipal city where station is geographically located."],
    ["stations", "state", "VARCHAR(100)", "NOT NULL", "State or Union Territory location."],
    # 2. routes
    ["routes", "route_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for route corridor."],
    ["routes", "route_code", "VARCHAR(30)", "UNIQUE, NOT NULL", "Alphanumeric route corridor identifier."],
    ["routes", "source_station_id", "INT", "FK, NOT NULL", "Origin station reference (stations.station_id)."],
    ["routes", "destination_station_id", "INT", "FK, NOT NULL", "Terminating station reference (stations.station_id)."],
    ["routes", "total_distance_km", "DECIMAL(7,2)", "CHECK (> 0), NOT NULL", "Total corridor track distance in kilometers."],
    # 3. train_stops
    ["train_stops", "stop_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for train halt."],
    ["train_stops", "route_id", "INT", "FK, NOT NULL", "Route corridor reference (routes.route_id)."],
    ["train_stops", "station_id", "INT", "FK, NOT NULL", "Station halt reference (stations.station_id)."],
    ["train_stops", "stop_sequence", "INT", "CHECK (> 0), NOT NULL", "Monotonically increasing stop sequence index."],
    ["train_stops", "distance_from_source_km", "DECIMAL(7,2)", "CHECK (>= 0), NOT NULL", "Cumulative track distance from route origin."],
    ["train_stops", "arrival_time", "TIME", "NULL", "Scheduled train arrival timetable time."],
    ["train_stops", "departure_time", "TIME", "NULL", "Scheduled train departure timetable time."],
    # 4. trains
    ["trains", "train_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for train definition."],
    ["trains", "train_number", "VARCHAR(10)", "UNIQUE, NOT NULL", "Official 5-digit Indian Railways train number."],
    ["trains", "train_name", "VARCHAR(100)", "NOT NULL", "Commercial train name (e.g., 'Vande Bharat Express')."],
    ["trains", "train_type", "VARCHAR(30)", "NOT NULL", "Operational train category (e.g., 'Superfast')."],
    ["trains", "route_id", "INT", "FK, NOT NULL", "Assigned route corridor (routes.route_id)."],
    # 5. train_runs
    ["train_runs", "run_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for dated train run."],
    ["train_runs", "train_id", "INT", "FK, NOT NULL", "Train definition reference (trains.train_id)."],
    ["train_runs", "run_date", "DATE", "NOT NULL", "Calendar date of train departure."],
    ["train_runs", "status", "VARCHAR(20)", "DEFAULT 'SCHEDULED'", "Operational status (SCHEDULED, COMPLETED, CANCELLED)."],
    # 6. coaches
    ["coaches", "coach_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for coach instance."],
    ["coaches", "train_id", "INT", "FK, NOT NULL", "Train reference (trains.train_id)."],
    ["coaches", "coach_code", "VARCHAR(10)", "NOT NULL", "Physical coach identifier (e.g., 'C1', 'B1')."],
    ["coaches", "travel_class", "VARCHAR(10)", "NOT NULL", "Class of travel (1A, 2A, 3A, CC, SL)."],
    ["coaches", "total_seats", "INT", "CHECK (> 0), DEFAULT 72", "Physical passenger seating capacity."],
    # 7. seats
    ["seats", "seat_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for seat berth."],
    ["seats", "coach_id", "INT", "FK, NOT NULL", "Coach reference (coaches.coach_id)."],
    ["seats", "seat_number", "INT", "CHECK (> 0), NOT NULL", "Berth number within coach (1 to 72)."],
    ["seats", "berth_type", "VARCHAR(15)", "NOT NULL", "Berth orientation (LOWER, UPPER, MIDDLE, SIDE LOWER, SIDE UPPER)."],
    # 8. passengers
    ["passengers", "passenger_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for passenger master."],
    ["passengers", "full_name", "VARCHAR(100)", "NOT NULL", "Full legal passenger name."],
    ["passengers", "gender", "VARCHAR(10)", "NOT NULL", "Passenger gender identity."],
    ["passengers", "age", "INT", "CHECK (age > 0 AND age < 120)", "Passenger age in years."],
    ["passengers", "email", "VARCHAR(120)", "NOT NULL, INDEX", "Contact email address for ERS notifications."],
    ["passengers", "phone", "VARCHAR(20)", "NOT NULL", "Contact phone number for journey alerts."],
    ["passengers", "id_card_type", "VARCHAR(20)", "NOT NULL", "Government ID type (AADHAAR, PAN, PASSPORT)."],
    ["passengers", "id_card_number", "VARCHAR(50)", "NOT NULL", "Government ID identification number."],
    # 9. fare_rules
    ["fare_rules", "fare_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for tariff rule."],
    ["fare_rules", "train_type", "VARCHAR(30)", "NOT NULL", "Train classification type."],
    ["fare_rules", "travel_class", "VARCHAR(10)", "NOT NULL", "Accommodation class category."],
    ["fare_rules", "base_fare", "DECIMAL(10,2)", "CHECK (>= 0), NOT NULL", "Base ticket reservation charge."],
    ["fare_rules", "rate_per_km", "DECIMAL(6,2)", "CHECK (>= 0), NOT NULL", "Per-kilometer distance rate."],
    ["fare_rules", "reservation_fee", "DECIMAL(6,2)", "CHECK (>= 0), DEFAULT 40.00", "Flat mandatory reservation charge."],
    # 10. bookings
    ["bookings", "booking_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for reservation."],
    ["bookings", "pnr_number", "VARCHAR(12)", "UNIQUE, NOT NULL", "10-digit Passenger Name Record string."],
    ["bookings", "run_id", "INT", "FK, NOT NULL", "Associated train run (train_runs.run_id)."],
    ["bookings", "passenger_id", "INT", "FK, NOT NULL", "Passenger master reference (passengers.passenger_id)."],
    ["bookings", "origin_station_id", "INT", "FK, NOT NULL", "Origin boarding station reference."],
    ["bookings", "destination_station_id", "INT", "FK, NOT NULL", "Destination debarking station reference."],
    ["bookings", "origin_stop_seq", "INT", "NOT NULL", "Boarding station stop sequence index."],
    ["bookings", "destination_stop_seq", "INT", "NOT NULL", "Debarking station stop sequence index."],
    ["bookings", "travel_class", "VARCHAR(10)", "NOT NULL", "Class booked (1A, 2A, 3A, CC, SL)."],
    ["bookings", "booking_status", "VARCHAR(20)", "DEFAULT 'CONFIRMED'", "Status (CONFIRMED, WAITLISTED, CANCELLED)."],
    ["bookings", "total_fare", "DECIMAL(10,2)", "CHECK (>= 0), NOT NULL", "Calculated ticket fare in INR."],
    ["bookings", "booked_at", "DATETIME", "NOT NULL, DEFAULT NOW", "Timestamp of booking transaction."],
    # 11. journey_segments
    ["journey_segments", "segment_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for berth allocation."],
    ["journey_segments", "booking_id", "INT", "FK, NOT NULL", "Associated booking reference."],
    ["journey_segments", "seat_id", "INT", "FK, NOT NULL", "Allocated physical berth reference."],
    ["journey_segments", "run_id", "INT", "FK, NOT NULL", "Dated train run reference."],
    ["journey_segments", "start_stop_seq", "INT", "NOT NULL", "Origin station stop sequence number."],
    ["journey_segments", "end_stop_seq", "INT", "NOT NULL", "Destination station stop sequence number."],
    ["journey_segments", "allocation_status", "VARCHAR(20)", "DEFAULT 'ACTIVE'", "Status of berth allocation (ACTIVE, CANCELLED)."],
    # 12. waitlists
    ["waitlists", "waitlist_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for waitlist ticket."],
    ["waitlists", "booking_id", "INT", "FK, NOT NULL", "Waitlisted booking header reference."],
    ["waitlists", "run_id", "INT", "FK, NOT NULL", "Dated train run reference."],
    ["waitlists", "travel_class", "VARCHAR(10)", "NOT NULL", "Class for which waitlisted."],
    ["waitlists", "origin_stop_seq", "INT", "NOT NULL", "Boarding stop sequence index."],
    ["waitlists", "destination_stop_seq", "INT", "NOT NULL", "Debarking stop sequence index."],
    ["waitlists", "position", "INT", "CHECK (> 0), NOT NULL", "Numerical FIFO queue priority position."],
    ["waitlists", "waitlist_status", "VARCHAR(20)", "DEFAULT 'WAITING'", "Status (WAITING, PROMOTED, CANCELLED)."],
    ["waitlists", "created_at", "DATETIME", "NOT NULL, DEFAULT NOW", "Timestamp of waitlist entry."],
    # 13. payments
    ["payments", "payment_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for payment entry."],
    ["payments", "booking_id", "INT", "FK, NOT NULL", "Associated booking reference."],
    ["payments", "amount", "DECIMAL(10,2)", "CHECK (>= 0), NOT NULL", "Total amount charged in INR."],
    ["payments", "payment_method", "VARCHAR(30)", "DEFAULT 'SIMULATED_UPI'", "Payment gateway or method."],
    ["payments", "transaction_reference", "VARCHAR(60)", "UNIQUE, NOT NULL", "Deterministic payment transaction reference."],
    ["payments", "payment_status", "VARCHAR(20)", "DEFAULT 'COMPLETED'", "Payment state (COMPLETED, REFUNDED)."],
    ["payments", "paid_at", "DATETIME", "NOT NULL, DEFAULT NOW", "Timestamp of successful transaction."],
    # 14. cancellations
    ["cancellations", "cancellation_id", "INT", "PK, AUTO_INCREMENT", "Surrogate unique key for cancellation entry."],
    ["cancellations", "booking_id", "INT", "FK, UNIQUE, NOT NULL", "Cancelled booking reference."],
    ["cancellations", "cancellation_reason", "VARCHAR(255)", "NOT NULL", "User-specified cancellation reason."],
    ["cancellations", "cancellation_fee", "DECIMAL(10,2)", "CHECK (>= 0), DEFAULT 0", "Deducted penalty amount (20%)."],
    ["cancellations", "refund_amount", "DECIMAL(10,2)", "CHECK (>= 0), NOT NULL", "Net amount refunded to passenger (80%)."],
    ["cancellations", "refund_status", "VARCHAR(20)", "DEFAULT 'PROCESSED'", "Refund processing state."],
    ["cancellations", "cancelled_at", "DATETIME", "NOT NULL, DEFAULT NOW", "Timestamp of cancellation transaction."]
]

# -------------------------------------------------------------------------
# TABLE 9: DATABASE IMPLEMENTATION ENVIRONMENT
# -------------------------------------------------------------------------
TABLE_9_HEADERS = ["Item", "Details"]
TABLE_9_ROWS = [
    ["DBMS Engine", "MySQL 8.0.36 Community Server / SQLite 3.39 (Development)"],
    ["Transactional Storage Engine", "InnoDB (ACID Compliant, Row-Level Locking, Crash Recovery)"],
    ["Character Set / Collation", "utf8mb4 / utf8mb4_unicode_ci"],
    ["Total Relational Tables", "14 Normalized Relations (Third Normal Form Compliant)"],
    ["Database Views", "3 Pre-Compiled Views (vw_confirmed_segments, vw_booking_summary, vw_train_occupancy_summary)"],
    ["Isolation Level", "READ COMMITTED / REPEATABLE READ with SELECT FOR UPDATE row locks"]
]

# -------------------------------------------------------------------------
# TABLE 10: APPLICATION DEVELOPMENT ENVIRONMENT
# -------------------------------------------------------------------------
TABLE_10_HEADERS = ["Item", "Details"]
TABLE_10_ROWS = [
    ["Programming Language", "Python 3.9.6 (64-bit)"],
    ["Web Framework", "Flask 3.1.3 (WSGI Microframework with Modular Blueprints)"],
    ["Object-Relational Mapping (ORM)", "SQLAlchemy 2.0.54 / Flask-SQLAlchemy 3.1.1"],
    ["Database Drivers", "PyMySQL 1.2.3 (MySQL) / sqlite3 (Built-in Standard Library)"],
    ["Front-End Architecture", "HTML5, CSS3, Bootstrap 5.3.3, Jinja2 Templates, JavaScript"],
    ["Testing & Verification Framework", "pytest 8.4.2 (16 Automated Integration & Unit Tests)"],
    ["Execution Operating System", "macOS Darwin 24.x (Apple Silicon arm64)"]
]

# -------------------------------------------------------------------------
# TABLE 11: APPLICATION MODULE-TO-DATABASE MAPPING
# -------------------------------------------------------------------------
TABLE_11_HEADERS = ["Module / Screen", "Purpose", "Tables Used", "Main Operations"]
TABLE_11_ROWS = [
    ["Dashboard & KPIs (`/`)", "Executive operational overview displaying revenue, bookings, and occupancy.", "bookings, train_runs, payments, waitlists", "SELECT aggregate queries, COUNT(), SUM(), GROUP BY"],
    ["Train Search (`/search`)", "Discovery engine for routes, stop sequences, and seat availability.", "trains, train_stops, stations, train_runs, coaches, seats, journey_segments", "Multi-table JOINs, interval non-overlap subquery checks"],
    ["Booking Flow (`/book`)", "Transaction-safe berth reservation, PNR generation, and payment.", "passengers, bookings, journey_segments, payments, seats", "INSERT passenger/booking, SELECT FOR UPDATE row lock, INSERT segment/payment"],
    ["Ticket ERS Slip (`/booking/<pnr>`)", "Official reservation slip retrieval and printable ticket display.", "bookings, passengers, train_runs, trains, journey_segments, seats, coaches, stations", "SELECT joined itinerary details by unique PNR number"],
    ["Waitlist Queue (`/waitlist`)", "Live monitoring of waiting list passengers and FIFO queue order.", "waitlists, bookings, passengers, train_runs, trains", "SELECT FIFO ordered queue records by run_id and class"],
    ["Cancellations (`/cancel`)", "Ticket cancellation, refund processing, and automated waitlist promotion.", "cancellations, bookings, journey_segments, waitlists, payments", "UPDATE booking/segment status, INSERT cancellation, SELECT and UPDATE waitlist"],
    ["SQL Analytics (`/reports`)", "Interactive execution console for 12 benchmark business SQL queries.", "All 14 relations + database views", "Complex nested queries, aggregations, HAVING, window functions"],
    ["Admin Explorer (`/admin`)", "Table row counters, schema exploration, and manual seed runner.", "All 14 relations", "SELECT COUNT(*) per table, DDL schema introspection"]
]

# -------------------------------------------------------------------------
# TABLE 12: CRUD OPERATIONS
# -------------------------------------------------------------------------
TABLE_12_HEADERS = ["Operation", "Application Feature / Screen", "Table(s) Affected", "Evidence"]
TABLE_12_ROWS = [
    ["Create (Insert)", "Booking Reservation Checkout (`/book/<run_id>`)", "passengers, bookings, journey_segments, payments", "Passenger record created, 10-digit PNR generated, active segments locked, and payment log committed atomically."],
    ["Create (Insert)", "Waitlist Enrolment (`/book/<run_id>`)", "bookings, waitlists, payments", "When class capacity is full, passenger is inserted into waitlists with calculated FIFO position."],
    ["Read (Select)", "Train Availability Search (`/search`)", "trains, routes, train_stops, train_runs, seats, journey_segments", "Evaluates half-open intervals [s, e) using NOT EXISTS overlap subqueries to retrieve available berths."],
    ["Read (Select)", "PNR Status & ERS View (`/booking/<pnr>`)", "bookings, passengers, train_runs, seats, stations", "Retrieves complete passenger manifest, travel dates, coach codes, and seat numbers."],
    ["Update (Modify)", "Waitlist Passenger Promotion (`/cancel/<pnr>`)", "bookings, journey_segments, waitlists", "Waitlist booking updated from WAITLISTED to CONFIRMED, segment created, and waitlist status updated to PROMOTED."],
    ["Delete / Cancel (Soft)", "Booking Cancellation (`/cancel/<pnr>`)", "bookings, journey_segments, cancellations", "Booking marked CANCELLED, segment allocation set to CANCELLED, freeing berth for reuse; cancellation fee logged."]
]

# -------------------------------------------------------------------------
# TABLE 13: BUSINESS RULES, VALIDATION AND ERROR HANDLING
# -------------------------------------------------------------------------
TABLE_13_HEADERS = ["Rule / Validation", "How Implemented", "Evidence / Message"]
TABLE_13_ROWS = [
    ["Forward Travel Rule", "Application check verifying destination_stop_seq > origin_stop_seq.", "Rejects backward searches with: 'Destination station must appear after origin station on route.'"],
    ["Interval Overlap Rule", "SQL subquery checking NOT (s_new < segment.end_seq AND e_new > segment.start_seq).", "Prevents double-booking: returns only berths with zero overlapping active allocations."],
    ["Waitlist FIFO Rule", "SQL query ordered by created_at ASC and position ASC during promotion.", "Promotes the earliest waiting passenger when an active confirmed seat is vacated."],
    ["Cancellation Penalty Rule", "Computes cancellation_fee = 0.20 * total_fare and refund = total_fare - fee.", "Flash message: 'Booking cancelled successfully. Refund of INR 619.20 processed (Fee: INR 154.80).'"],
    ["Single Cancellation Rule", "UNIQUE constraint on cancellations.booking_id and status guard.", "Rejects duplicate cancellations with: 'This booking has already been cancelled.'"],
    ["Domain Age Validation", "CHECK constraint (age > 0 AND age < 120) and WTForms integer validator.", "Rejects invalid age inputs with: 'Passenger age must be a valid number between 1 and 119.'"],
    ["Transaction Atomicity", "Database transaction block wrapped in try-except with db.session.rollback().", "If payment logging fails, booking and segment allocations are cleanly rolled back."]
]

# -------------------------------------------------------------------------
# TABLE 14: REPORTS AND DATABASE OPERATIONS
# -------------------------------------------------------------------------
TABLE_14_HEADERS = ["Report / Operation", "SQL / Database Concept Used", "Application Output"]
TABLE_14_ROWS = [
    ["Report 1: Segment-Wise Seat Availability", "Aggregations, COUNT(DISTINCT), LEFT JOIN, GROUP BY", "Tabular breakdown of total seats, active allocations, and vacant seats per train run."],
    ["Report 2: Passenger Booking History", "Multi-table INNER JOINs, ORDER BY, Date Formatting", "Chronological audit trail of all issued tickets with PNR, passenger names, and fares."],
    ["Report 3: Active Waitlist Queue Priority", "FIFO Queue Ordering, Joins, WHERE status = 'WAITING'", "Real-time list of passengers awaiting berth clearance ordered by queue position."],
    ["Report 4: Route Revenue & Financial Yield", "SUM(total_fare), JOIN across bookings and routes, GROUP BY", "Corridor financial yield ranking routes by cumulative passenger revenue generated."],
    ["Report 5: Train Occupancy Load Factor", "Derived metrics, COUNT() / capacity ratios, HAVING", "Capacity utilization percentage across all dated train runs and coach classes."],
    ["Report 6: Station Transit Passenger Density", "UNION ALL of boarding and debarking station counts, GROUP BY", "Identifies highest-density interchange hubs based on passenger footfall."],
    ["Report 7: Berth Preference Distribution", "COUNT(), GROUP BY berth_type, percentage share calculation", "Distribution analysis showing passenger demand for Lower, Upper, and Side berths."],
    ["Report 8: Cancellation & Refund Financial Audit", "SUM(cancellation_fee), SUM(refund_amount), JOINs", "Financial accounting of total fees retained vs total funds refunded to passengers."],
    ["Report 9: Frequent Traveler Loyalty Tiers", "COUNT(booking_id), CASE statements, HAVING bookings >= 1", "Categorizes travelers into Platinum, Gold, and Silver loyalty tiers."],
    ["Report 10: Peak vs Off-Peak Travel Demand", "EXTRACT(DOW), COUNT(), GROUP BY day of week", "Analysis of weekend vs weekday passenger travel patterns across all corridors."],
    ["Report 11: Waitlist Clearance Success Rate", "Conditional SUM(CASE WHEN status = 'PROMOTED'), percentage", "Operational KPI measuring percentage of waitlisted passengers successfully promoted."],
    ["Report 12: High-Value Passenger Bookings", "Correlated Subquery, WHERE total_fare > (SELECT AVG(total_fare))", "Filters premium bookings exceeding system-wide average ticket fare."]
]

# -------------------------------------------------------------------------
# TABLE 15: TEST CASES
# -------------------------------------------------------------------------
TABLE_15_HEADERS = ["Test ID", "Feature", "Input / Action", "Expected Result", "Actual Result", "Status"]
TABLE_15_ROWS = [
    ["TC-01", "Interval Overlap Detection", "Test [1,2) vs [2,4) and [1,3) vs [2,4)", "[1,2) does not overlap; [1,3) overlaps [2,4)", "Overlap theorem evaluated correctly", "PASSED"],
    ["TC-02", "Non-Overlapping Seat Reuse", "Book C1-1 on [1,2), then book C1-1 on [2,4)", "Both allocations active concurrently on same seat", "Both allocations confirmed in database", "PASSED"],
    ["TC-03", "Conflicting Interval Detection", "Book C1-1 on [1,4) when [1,2) already booked", "System identifies seat as conflicting / unavailable", "Conflict detected; seat excluded from available list", "PASSED"],
    ["TC-04", "Cancelled Allocation Reuse", "Cancel booking on C1-3, search [1,4)", "C1-3 is returned as available for re-booking", "Availability restored; seat returned in query", "PASSED"],
    ["TC-05", "Cancellation Refund Policy", "Cancel confirmed booking with fare INR 774", "20% fee (INR 154.80) deducted, 80% (INR 619.20) refunded", "Fee and refund amounts logged accurately", "PASSED"],
    ["TC-06", "Duplicate Cancellation Prevention", "Cancel already cancelled booking", "ValueError raised; duplicate cancellation blocked", "ValueError caught; duplicate operation prevented", "PASSED"],
    ["TC-07", "Automated Waitlist Promotion", "Cancel confirmed seat with waiting candidate", "Candidate promoted to CONFIRMED, segment created", "Candidate promoted; queue position cleared", "PASSED"],
    ["TC-08", "Unique Train Number Constraint", "Insert duplicate train_number '22436'", "IntegrityError raised by RDBMS UNIQUE constraint", "IntegrityError raised; duplicate rejected", "PASSED"],
    ["TC-09", "Foreign Key Referential Integrity", "Insert coach with non-existent train_id 9999", "IntegrityError raised on foreign key violation", "IntegrityError raised; orphan coach blocked", "PASSED"],
    ["TC-10", "Passenger Age Domain Constraint", "Insert passenger with age = 150", "IntegrityError raised by CHECK (age < 120)", "IntegrityError raised; invalid age rejected", "PASSED"],
    ["TC-11", "Negative Base Fare Constraint", "Insert fare_rule with base_fare = -50.00", "IntegrityError raised by CHECK (base_fare >= 0)", "IntegrityError raised; negative fare rejected", "PASSED"],
    ["TC-12", "Duplicate Stop Sequence Rejection", "Insert two stops with same (route_id, stop_seq)", "IntegrityError raised by UNIQUE constraint", "IntegrityError raised; sequence collision blocked", "PASSED"],
    ["TC-13", "SQL Benchmark Reports Execution", "Execute all 12 benchmark SQL analytical queries", "All 12 queries return valid result sets", "All 12 queries executed without error", "PASSED"],
    ["TC-14", "Atomic Booking Transaction", "Book ticket with valid passenger details", "Booking, segment, and payment committed together", "All records committed; PNR generated", "PASSED"],
    ["TC-15", "Invalid Travel Direction Check", "Book journey where dest_stop_seq < orig_stop_seq", "ValueError raised; backward travel rejected", "ValueError caught; invalid booking blocked", "PASSED"],
    ["TC-16", "Train Run Isolation Check", "Book same seat C1-1 on Run A (Day 1) and Run B (Day 2)", "Both bookings confirmed without conflict", "Both bookings active on their respective dates", "PASSED"]
]

# -------------------------------------------------------------------------
# IEEE REFERENCES
# -------------------------------------------------------------------------
IEEE_REFERENCES = [
    "[1] E. F. Codd, “A relational model of data for large shared data banks,” Communications of the ACM, vol. 13, no. 6, pp. 377–387, Jun. 1970, doi: 10.1145/362384.362685.",
    "[2] C. J. Date, An Introduction to Database Systems, 8th ed. Boston, MA, USA: Addison-Wesley, 2004.",
    "[3] A. Silberschatz, H. F. Korth, and S. Sudarshan, Database System Concepts, 7th ed. New York, NY, USA: McGraw-Hill Education, 2020.",
    "[4] R. Elmasri and S. B. Navathe, Fundamentals of Database Systems, 7th ed. Boston, MA, USA: Pearson, 2016.",
    "[5] Oracle Corporation, MySQL 8.0 Reference Manual: InnoDB Storage Engine Architecture and Concurrency, Redwood Shores, CA, USA, 2024. [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/",
    "[6] Pallets Projects, Flask Documentation (v3.1.x): Application Context, Blueprints, and Database Handling, 2024. [Online]. Available: https://flask.palletsprojects.com/",
    "[7] M. Bayer, SQLAlchemy Documentation: Transaction Management and ORM Mapping, 2024. [Online]. Available: https://docs.sqlalchemy.org/",
    "[8] H. Krekel et al., pytest: Python Testing Framework Documentation, ver. 8.4, 2024. [Online]. Available: https://docs.pytest.org/",
    "[9] M. Stonebraker, “The design of the POSTGRES storage system,” in Proc. 13th Int. Conf. Very Large Data Bases (VLDB), 1987, pp. 289–300.",
    "[10] J. Gray and A. Reuter, Transaction Processing: Concepts and Techniques. San Francisco, CA, USA: Morgan Kaufmann, 1993."
]

print("Loaded all structured PBL report datasets successfully.")
