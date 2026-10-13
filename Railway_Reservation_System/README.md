# Railway Ticket Reservation and Journey Management System
**Student Name:** Heman | **Roll Number:** 25WU0102097 | **Section:** AIML Rhinos  
**Faculty Mentor:** Prof. Sahithi  
**Academic Coursework:** Database Management Systems (DBMS) — B.Tech CSE (AIML)  
**RDBMS Target:** MySQL 8.x (InnoDB Transactional Storage Engine) with SQLite Local Dev Mode  
**Normalization:** Third Normal Form (3NF)  

---

## 1. Project Overview

The **Railway Ticket Reservation and Journey Management System** is a complete, full-stack relational database project engineered to solve the complex inventory allocation problems inherent to multi-hop passenger transport.

Unlike airline seating where an entire flight is booked as a single block, railway trains travel through ordered sequences of intermediate stations. A single physical berth may be allocated to distinct passengers on disjoint, non-overlapping segments, yet must strictly reject any overlapping allocations.

### Key Capabilities Demonstrated:
- **Segment-Wise Half-Open Interval Allocation:** Seats are modeled over $[start\_stop\_seq, end\_stop\_seq)$. Overlap test: $s < r_{end} \land r_{start} < e$.
- **ACID Concurrency Safety:** Pessimistic row locking (`SELECT ... FOR UPDATE`) serializes competing seat reservation requests.
- **Third Normal Form (3NF) Schema:** 14 decoupled relations separating train catalogs from dated runs, passengers from bookings, and tariff rules from payment logs.
- **Automated Waitlist Promotion:** Cancellations trigger atomic re-evaluation of waiting candidates in strict FIFO priority order.
- **12 SQL Analytics Reports:** Benchmark joins, aggregations, views, and financial reconciliation.
- **Full Academic Deliverables:** 3 editable PowerPoint presentations, comprehensive Word project report, data dictionary, viva question bank, and 16 automated tests.

---

## 2. Directory Structure

```text
Railway_Reservation_System/
├── app/
│   ├── __init__.py                 # Flask factory & SQLite PRAGMA FK hook
│   ├── config.py                   # App config (MySQL & SQLite fallback)
│   ├── extensions.py               # SQLAlchemy instance
│   ├── models/                     # 14 SQLAlchemy Relational Models (3NF)
│   │   ├── station.py, route.py, train.py, schedule.py, coach.py
│   │   ├── passenger.py, fare.py, booking.py, journey_segment.py
│   │   └── waitlist.py, payment.py, cancellation.py
│   ├── services/                   # Core Relational Business Logic
│   │   ├── availability_service.py # Half-open interval overlap algorithm
│   │   ├── booking_service.py      # Transaction-safe reservation & row locking
│   │   ├── cancellation_service.py # Refund policy & atomic waitlist promotion
│   │   ├── fare_service.py         # Distance & class tariff calculator
│   │   └── report_service.py       # 12 SQL benchmark analytics queries
│   ├── routes/                     # Modular Flask Blueprints
│   │   ├── main_routes.py, train_routes.py, passenger_routes.py
│   │   ├── booking_routes.py, cancellation_routes.py, waitlist_routes.py
│   │   ├── report_routes.py, admin_routes.py
│   │   └── templates/ & static/    # Jinja2 templates & CSS/JS UI
├── database/
│   ├── schema.sql                  # MySQL 8.x InnoDB DDL (PK, FK, CHECK, INDEX)
│   ├── views.sql                   # Relational views for operational reporting
│   ├── reports.sql                 # 12 Benchmark SQL query scripts
│   └── seed_data.py                # Benchmark dataset seeder
├── tests/
│   ├── conftest.py                 # Pytest fixtures
│   ├── test_integrity.py           # DDL & constraint rejection tests
│   ├── test_availability.py        # Interval overlap & seat reuse tests
│   ├── test_reservations.py        # Booking workflows & run isolation
│   ├── test_cancellations.py       # Refund policy & atomic promotion
│   └── test_reports.py             # All 12 SQL report execution tests
├── docs/
│   ├── project_report.docx         # Comprehensive 23-section Academic Report
│   ├── data_dictionary.md          # Full attribute-level schema dictionary
│   ├── functional_dependencies.md  # Formal FDs & 3NF decomposition proofs
│   ├── test_results.md             # Execution log of 16 passed tests
│   ├── demo_script.md              # 5-8 minute live presentation script
│   ├── viva_qa.md                  # 21 Viva Q&A + 5 Deep-dive defenses
│   └── screenshots/                # Real captured application screenshots
├── presentations/
│   ├── Review_1_Requirements_and_ER_Design.pptx          # Review 1 (11 slides)
│   ├── Review_2_Normalization_and_SQL_Implementation.pptx# Review 2 (12 slides)
│   └── Review_3_Final_Implementation_and_Demo.pptx       # Review 3 (12 slides)
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py                          # Application startup & auto-seeder
└── README.md
```

---

## 3. Quickstart & Installation

### Step 1: Clone or Navigate to Directory
```bash
cd "Railway_Reservation_System"
```

### Step 2: Create and Activate Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
- **Option A (SQLite Local Development - Default):** Works out of the box with zero external configuration! SQLite foreign key pragma (`PRAGMA foreign_keys = ON;`) is enabled automatically on every connection to emulate InnoDB constraints.
- **Option B (MySQL 8.x Production Target):** Edit `.env` to configure your MySQL connection:
  ```env
  DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/railway_db
  ```
  Create database in MySQL:
  ```sql
  CREATE DATABASE railway_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

### Step 5: Start Application
```bash
python run.py
```
*The application initializes all 14 database tables and seeds the benchmark demonstration data automatically on first launch.*

Open your browser to:
👉 **`http://127.0.0.1:5001/`**

---

## 4. Running Automated Tests

Execute the automated test suite using `pytest`:
```bash
pytest tests -v
```

### Expected Output:
```text
tests/test_availability.py::test_interval_overlap_logic PASSED
tests/test_availability.py::test_non_overlapping_seat_reuse PASSED
tests/test_availability.py::test_conflicting_interval_detection PASSED
tests/test_availability.py::test_cancelled_allocation_restores_availability PASSED
tests/test_cancellations.py::test_eligible_cancellation_and_refund_policy PASSED
tests/test_cancellations.py::test_duplicate_cancellation_rejected PASSED
tests/test_cancellations.py::test_automated_waitlist_promotion PASSED
tests/test_integrity.py::test_unique_train_number_constraint PASSED
tests/test_integrity.py::test_invalid_foreign_key_rejected PASSED
tests/test_integrity.py::test_passenger_age_check_constraint PASSED
tests/test_integrity.py::test_negative_fare_check_constraint PASSED
tests/test_integrity.py::test_duplicate_stop_sequence_rejected PASSED
tests/test_reports.py::test_all_12_reports_execute_successfully PASSED
tests/test_reservations.py::test_valid_booking_success PASSED
tests/test_reservations.py::test_invalid_origin_dest_sequence_fails PASSED
tests/test_reservations.py::test_train_runs_isolation PASSED
============================== 16 passed in 0.36s ==============================
```

---

## 5. Live Demonstration Sequence (5–8 Minutes)

1. **Dashboard (`/`):** View dynamic metrics: Active Trains (3), Passengers (8), Confirmed Bookings (3), Waitlist (1), Cancellations (1), and Net Retained Revenue (₹5,106.80).
2. **Train Search (`/search`):** Search from `NDLS` (New Delhi) to `BSB` (Varanasi Junction) on `2026-10-14`. Observe matching train 22436 (Vande Bharat Express) and class availability cards (CC, 1A).
3. **Confirmed Booking (`/book`):** Select passenger `Rajesh Kumar`, choose travel class `CC`, view calculated fare, and confirm reservation. Renders Electronic Reservation Slip (ERS) with 10-digit PNR and Coach/Seat allocation.
4. **Non-Overlapping Seat Reuse Proof:** In the seed dataset:
   - Passenger 1 (Aarav Sharma) holds Seat `C1-1` on segment $[1, 2)$ (`NDLS` -> `CNB`).
   - Passenger 2 (Priya Patel) holds the **exact same Seat `C1-1`** on segment $[2, 4)$ (`CNB` -> `BSB`).
   - Both co-exist actively because $[1, 2)$ and $[2, 4)$ do not overlap!
5. **Cancellation & Waitlist Promotion (`/cancel`):** Cancel a confirmed booking. Observe policy enforcement (20% fee deduction, 80% refund) and instant atomic promotion of the top waitlisted candidate (`/waitlist`).
6. **SQL Reports Hub (`/reports`):** Run all 12 benchmark queries, including coach occupancy percentage and revenue reconciliation.

---

## 6. Academic Deliverables & Course Artifacts

| Deliverable | File Path | Focus |
|---|---|---|
| **Review 1 Presentation** | `presentations/Review_1_Requirements_and_ER_Design.pptx` | Week 7 (5 Marks): Requirements, Scope, Business Rules, ER Diagram |
| **Review 2 Presentation** | `presentations/Review_2_Normalization_and_SQL_Implementation.pptx` | Week 11 (5 Marks): 3NF Normalization, DDL, SQL Queries, Test Evidence |
| **Review 3 Presentation** | `presentations/Review_3_Final_Implementation_and_Demo.pptx` | Week 16 (5 Marks): Full System Demo, Embedded Screenshots, Testing, Viva Prep |
| **Academic Project Report**| `docs/project_report.docx` | Full 23-Section Formal B.Tech Project Report with Figures & Tables |
| **Relational Data Dictionary**| `docs/data_dictionary.md` | Full attribute types, keys, nullability, constraints, descriptions |
| **Normalization Proof** | `docs/functional_dependencies.md` | Minimal Candidate Keys, Functional Dependencies, 1NF/2NF/3NF Proof |
| **Viva Question Bank** | `docs/viva_qa.md` | 21 Core Conceptual Viva Q&A + 5 Challenging Deep-Dive Defenses |
| **Demo Script** | `docs/demo_script.md` | Step-by-step 5–8 minute live defense demonstration script |
| **Test Results** | `docs/test_results.md` | 16/16 Passed Pytest Execution Evidence & Log |
