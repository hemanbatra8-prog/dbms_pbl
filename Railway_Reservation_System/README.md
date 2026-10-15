<div align="center">

# 🚆 Railway Ticket Reservation & Journey Management System
### *Enterprise Relational Database Management System with Segment-Wise Interval Seat Allocation, Pessimistic ACID Concurrency & Automated Waitlist Promotion*

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL 8.0](https://img.shields.io/badge/MySQL-8.0%20InnoDB-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Zero--Config-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Schema 3NF](https://img.shields.io/badge/Schema-3NF%20Decoupled-success?style=for-the-badge&logo=databricks&logoColor=white)](docs/functional_dependencies.md)
[![pytest](https://img.shields.io/badge/pytest-16%20Passed%20(100%25)-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](docs/test_results.md)
[![Woxsen University](https://img.shields.io/badge/Woxsen%20University-School%20of%20Technology-E31837?style=for-the-badge)](https://woxsen.edu.in/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

### **DBMS Project-Based Learning (PBL) Coursework**
**School of Technology, Woxsen University, Hyderabad (2026 – 2027)**

| Student Name | Roll Number | Program & Section | Faculty Mentor |
|:---:|:---:|:---:|:---:|
| **Heman** | `25WU0102097` | **B.Tech CSE (AIML)** — AIML Rhinos | **Prof. Sahithi** |

[📑 Official 40-Page Report (PDF)](Railway_Ticket_Reservation_DBMS_PBL_Report.pdf) • [📊 Review Presentations](presentations/) • [🧪 Automated Tests](docs/test_results.md) • [📖 Data Dictionary](docs/data_dictionary.md) • [💡 Viva Q&A](docs/viva_qa.md)

---

</div>

## 📑 Table of Contents
- [1. Executive Summary](#1-executive-summary)
- [2. Academic Review Presentations](#2-academic-review-presentations)
- [3. Core Technical Innovations](#3-core-technical-innovations)
- [4. Relational Database Architecture (14 Tables in 3NF)](#4-relational-database-architecture-14-tables-in-3nf)
- [5. Application UI & Screenshot Showcase](#5-application-ui--screenshot-showcase)
- [6. 12 Benchmark SQL Analytical Reports](#6-12-benchmark-sql-analytical-reports)
- [7. Quickstart & Installation](#7-quickstart--installation)
- [8. Automated Test Suite (16/16 Passed)](#8-automated-test-suite-1616-passed)
- [9. Repository Structure](#9-repository-structure)
- [10. Academic Deliverables & Course Artifacts](#10-academic-deliverables--course-artifacts)

---

## 1. Executive Summary

The **Railway Ticket Reservation and Journey Management System** is an end-to-end relational database application built to address the combinatorial challenges of intermediate station seat allocation in modern passenger rail networks.

Unlike airline reservation systems where a seat is locked for an entire non-stop flight, passenger trains travel through ordered sequences of intermediate stations ($s_1 \rightarrow s_2 \rightarrow s_3 \dots \rightarrow s_k$). Under a point-to-point booking strategy, allocating an entire journey to a single passenger causes severe seat wastage over intermediate segments. 

This project implements a **segment-wise half-open interval allocation algorithm** $[start\_stop\_seq, end\_stop\_seq)$, allowing the exact same physical berth to be allocated across disjoint segments to multiple passengers, while strictly rejecting any overlapping intervals under concurrent transactional load.

```
Station Sequence:  [1] New Delhi --------> [2] Kanpur --------> [3] Prayagraj --------> [4] Varanasi
Passenger A:       [========== Holds Berth C1-1 ==========)
Passenger B:                                                [========== Holds Berth C1-1 ==========)
Result:            ✅ 100% Valid (Disjoint Intervals [1, 2) and [2, 4) Co-exist on the Same Physical Seat!)
```

---

## 2. Academic Review Presentations

All three formal university evaluation slide decks are organized in the [`presentations/`](presentations/) directory with both **direct online PDF previews** and **editable PowerPoint PPTX files**:

| Review Milestone | Weighting & Week | PDF Online Preview | Editable PPTX Deck | Slides | Evaluation Focus |
|:---:|:---:|:---:|:---:|:---:|:---|
| **Review 1** | **Week 7** (5 Marks) | [📄 View Review 1 PDF](presentations/Review_1_Requirements_and_ER_Design.pdf) | [📥 Review 1 PPTX](presentations/Review_1_Requirements_and_ER_Design.pptx) | 11 | Problem Statement, Scope, Business Rules, ER Diagram (14 Relations), Cardinalities |
| **Review 2** | **Week 11** (5 Marks) | [📄 View Review 2 PDF](presentations/Review_2_Normalization_and_SQL_Implementation.pdf) | [📥 Review 2 PPTX](presentations/Review_2_Normalization_and_SQL_Implementation.pptx) | 12 | 3NF Decomposition, Functional Dependencies, DDL Constraints, 12 SQL Analytics |
| **Review 3** | **Week 16** (5 Marks) | [📄 View Review 3 PDF](presentations/Review_3_Final_Implementation_and_Demo.pdf) | [📥 Review 3 PPTX](presentations/Review_3_Final_Implementation_and_Demo.pptx) | 12 | Working Full-Stack System, Interval Math, ACID Concurrency, Waitlist Engine, Live Demo |

> 💡 *Visit the [presentations/README.md](presentations/README.md) catalog for detailed slide-by-slide agendas and oral defense notes.*

---

## 3. Core Technical Innovations

### 1. Segment-Wise Half-Open Interval Allocation Math
Seats are modeled as continuous segments across station sequence numbers $[start\_stop\_seq, end\_stop\_seq)$. Two booking requests for the same physical seat on intervals $[s_{req}, e_{req})$ and $[s_{curr}, e_{curr})$ conflict if and only if:

$$\text{Overlap}(req, curr) \iff s_{req} < e_{curr} \land s_{curr} < e_{req}$$

This condition prevents double bookings while dynamically maximizing seat utilization across intermediate station hops.

### 2. Pessimistic Concurrency & ACID Row Locking
Under concurrent reservation traffic, naive reads create severe race conditions (phantom seats and double allocations). This system utilizes **pessimistic row locking** via SQLAlchemy / MySQL:

```python
# Acquire exclusive write lock on active journey segments for dated train run
db.session.query(JourneySegment).filter(
    JourneySegment.run_id == run_id,
    JourneySegment.allocation_status == 'ACTIVE'
).with_for_update().all()
```

This guarantees serializable execution of concurrent booking requests, maintaining strict ACID guarantees across high-concurrency reservation windows.

### 3. Automated FIFO Waitlist Promotion Engine
When a passenger cancels a confirmed reservation:
1. The allocated seat intervals $[s, e)$ are marked `CANCELLED`.
2. Financial reconciliation executes atomically (20% flat cancellation fee retained, 80% net refund computed and logged).
3. The waitlist queue is queried in strict FIFO priority order (`position ASC`).
4. The first eligible candidate whose requested station interval fits into the vacated seat segments is atomically promoted to `CONFIRMED`.
5. Remaining waitlisted candidates have their queue positions decremented.

---

## 4. Relational Database Architecture (14 Tables in 3NF)

The schema is rigorously normalized to **Third Normal Form (3NF)** with complete transitive and partial dependency elimination.

```mermaid
erDiagram
    STATIONS ||--o{ ROUTES : "contains stops"
    TRAINS ||--o{ ROUTES : "operates along"
    TRAINS ||--o{ COACHES : "comprises"
    TRAINS ||--o{ TRAIN_RUNS : "scheduled on date"
    COACHES ||--o{ SEATS : "contains berths"
    PASSENGERS ||--o{ BOOKINGS : "books"
    TRAIN_RUNS ||--o{ BOOKINGS : "manifests"
    BOOKINGS ||--o{ JOURNEY_SEGMENTS : "allocates"
    SEATS ||--o{ JOURNEY_SEGMENTS : "occupies segment"
    BOOKINGS ||--o| PAYMENTS : "reconciles"
    BOOKINGS ||--o| CANCELLATIONS : "records refund"
    BOOKINGS ||--o| WAITLISTS : "queues if full"
    TRAINS ||--o{ FARE_RULES : "governs tariff"
```

### Table Summary Catalog

| # | Relation Name | Primary Key | Foreign Keys & References | Domain Responsibility |
|:---:|:---|:---|:---|:---|
| 1 | `stations` | `station_id` | *None* (Unique `station_code`) | Master station registry with GPS coordinates & timezone |
| 2 | `routes` | `route_id` | `train_id`, `station_id` | Intermediate train stops with arrival/departure & sequence index |
| 3 | `trains` | `train_id` | *None* (Unique `train_number`) | Train catalog master, service category & operating days |
| 4 | `train_runs` | `run_id` | `train_id` | Dated instances of scheduled train runs |
| 5 | `coaches` | `coach_id` | `train_id` | Physical coaches per train with class & total berth capacity |
| 6 | `seats` | `seat_id` | `coach_id` | Physical berth registry (berth number, type: LOWER, UPPER, SIDE) |
| 7 | `passengers` | `passenger_id` | *None* (Unique `email`, `phone`) | Passenger directory with identity proof and demographic attributes |
| 8 | `fare_rules` | `fare_id` | `train_type`, `travel_class` | Distance-based tariff pricing, base fares, and reservation fees |
| 9 | `bookings` | `booking_id` | `passenger_id`, `run_id`, `stations` | 10-digit unique PNR header, travel class, status, total fare |
| 10 | `journey_segments` | `segment_id` | `booking_id`, `seat_id`, `run_id` | Half-open intervals $[s, e)$ linking seats to station sequences |
| 11 | `waitlists` | `waitlist_id` | `booking_id`, `run_id` | Priority queue positions for overflow reservation requests |
| 12 | `payments` | `payment_id` | `booking_id` | Payment settlement ledger with deterministic transaction hashes |
| 13 | `cancellations` | `cancellation_id` | `booking_id` | Cancellation audit log, retained fee (20%), and net refund (80%) |
| 14 | `schema_migrations` | `migration_id` | *None* | Schema versioning and audit telemetry |

> 📖 *For complete column definitions, constraints, indices, and defaults, see the [Relational Data Dictionary](docs/data_dictionary.md).*

---

## 5. Application UI & Screenshot Showcase

| Figure 1: Relational Entity-Relationship Diagram (ERD) |
|:---:|
| ![Entity-Relationship Diagram](docs/screenshots/er_diagram.png) |
| *Full 14-table 3NF ER diagram detailing primary keys, composite foreign keys, and cardinalities.* |

<br>

| Figure 2: Executive Analytics Dashboard | Figure 3: Multi-Hop Train Search & Inventory |
|:---:|:---:|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Search Results](docs/screenshots/search_results.png) |
| *Real-time metrics: Active trains, passengers, bookings, retained revenue.* | *Intermediate station hop resolution and live seat availability cards.* |

<br>

| Figure 4: Confirmed ERS Ticket Slip | Figure 5: Live Waitlist Queue & Tracker |
|:---:|:---:|
| ![ERS Booking](docs/screenshots/booking_ers.png) | ![Waitlist Queue](docs/screenshots/waitlist_queue.png) |
| *Generated 10-digit PNR slip with coach/seat assignment and fare audit.* | *FIFO queue priority position tracking and candidate promotion state.* |

<br>

| Figure 6: SQL Analytical Reports Hub | Figure 7: Relational Schema & Admin Explorer |
|:---:|:---:|
| ![SQL Reports Console](docs/screenshots/sql_reports.png) | ![Admin Schema Explorer](docs/screenshots/schema_admin.png) |
| *Live execution console for all 12 benchmark business intelligence queries.* | *Live relational schema browser and train inventory control panel.* |

---

## 6. 12 Benchmark SQL Analytical Reports

The application provides pre-compiled analytical views and parameterized queries (`Railway_Reservation_System/database/reports.sql`) demonstrating advanced SQL mastery:

| Report # | Title | Key SQL Techniques Demonstrated | Business Objective |
|:---:|:---|:---|:---|
| **1** | Train Occupancy by Run | `INNER JOIN`, `COUNT(DISTINCT)`, `GROUP BY` | Track physical seat capacity utilization per dated run |
| **2** | Station Boarding & Debarking Flow | `LEFT JOIN`, `COALESCE`, `GROUP BY` | Analyze passenger ingress and egress traffic at each station |
| **3** | Gross & Net Revenue Reconciliation | `SUM`, `CASE WHEN`, `ROUND`, Aggregate Math | Compare gross bookings vs retained cancellation fees and refunds |
| **4** | Real-Time Waitlist Queue Priority | `SELECT`, `WHERE`, `ORDER BY position ASC` | Monitor pending waitlist demand and candidate priority |
| **5** | Route Punctuality & Duration Analysis | `TIMESTAMPDIFF`, Window Aggregation | Evaluate scheduled transit duration across route legs |
| **6** | Passenger Booking Frequency Matrix | `COUNT(b.booking_id)`, `HAVING COUNT > 1` | Identify frequent travelers and loyalty eligibility |
| **7** | Cancellation Pattern & Reason Audit | `GROUP BY cancellation_reason`, Percentage share | Audit operational drivers of journey cancellations |
| **8** | Class-Wise Fare Yield Analysis | `AVG(total_fare)`, `MIN`, `MAX` | Measure average revenue yield across 1A, 2A, 3A, CC, SL |
| **9** | Physical Berth Allocation Distribution | `GROUP BY berth_type`, `ORDER BY total DESC` | Identify passenger preferences for LOWER, UPPER, SIDE berths |
| **10** | Unutilized Seat Segments Detection | `NOT EXISTS`, Correlated Subquery | Isolate empty seats across intermediate station hops |
| **11** | Payment Settlement & Reconciliation | `GROUP BY payment_method, payment_status` | Gateway auditing, transaction verification, refund status |
| **12** | Peak Travel Day Demand Index | `DAYNAME(travel_date)`, `COUNT(*)` | Discover peak weekday booking patterns for capacity planning |

---

## 7. Quickstart & Installation

### Option A: Zero-Config Local Setup (SQLite Mode — Recommended)
Works out of the box with zero external dependencies!

```bash
# 1. Clone repository
git clone git@github.com:hemanbatra8-prog/dbms_pbl.git
cd dbms_pbl/Railway_Reservation_System

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch web application (auto-initializes tables & seeds benchmark dataset)
python run.py
```

Open your browser to:
👉 **`http://127.0.0.1:5001/`**

### Option B: Production MySQL 8.x Setup
Edit `.env` inside `Railway_Reservation_System/`:

```env
DATABASE_URL=mysql+pymysql://root:your_mysql_password@localhost:3306/railway_db
SECRET_KEY=production-secret-key-change-me
```

Create the database in MySQL:
```sql
CREATE DATABASE railway_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 8. Automated Test Suite (16/16 Passed)

The repository includes a comprehensive `pytest` test suite verifying database integrity constraints, interval overlap math, booking workflows, cancellation refunds, and report queries.

```bash
pytest tests -v
```

### Execution Log Evidence
```text
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2
tests/test_availability.py::test_interval_overlap_logic PASSED            [  6%]
tests/test_availability.py::test_non_overlapping_seat_reuse PASSED         [ 12%]
tests/test_availability.py::test_conflicting_interval_detection PASSED       [ 18%]
tests/test_availability.py::test_cancelled_allocation_restores_availability PASSED [ 25%]
tests/test_cancellations.py::test_eligible_cancellation_and_refund_policy PASSED [ 31%]
tests/test_cancellations.py::test_duplicate_cancellation_rejected PASSED   [ 37%]
tests/test_cancellations.py::test_automated_waitlist_promotion PASSED      [ 43%]
tests/test_integrity.py::test_unique_train_number_constraint PASSED       [ 50%]
tests/test_integrity.py::test_invalid_foreign_key_rejected PASSED          [ 56%]
tests/test_integrity.py::test_passenger_age_check_constraint PASSED         [ 62%]
tests/test_integrity.py::test_negative_fare_check_constraint PASSED       [ 68%]
tests/test_integrity.py::test_duplicate_stop_sequence_rejected PASSED      [ 75%]
tests/test_reports.py::test_all_12_reports_execute_successfully PASSED     [ 81%]
tests/test_reservations.py::test_valid_booking_success PASSED             [ 87%]
tests/test_reservations.py::test_invalid_origin_dest_sequence_fails PASSED [ 93%]
tests/test_reservations.py::test_train_runs_isolation PASSED              [100%]
============================== 16 passed in 0.38s ==============================
```

> 🧪 *For complete test scenario descriptions, see [docs/test_results.md](docs/test_results.md).*

---

## 9. Repository Structure

```text
dbms_pbl/
├── Railway_Ticket_Reservation_DBMS_PBL_Report.docx  # Official 40-Page Woxsen PBL Report (Word)
├── Railway_Ticket_Reservation_DBMS_PBL_Report.pdf   # Official 40-Page Woxsen PBL Report (PDF)
├── README.md                                        # Primary GitHub Showcase & Technical Documentation
├── presentations/                                   # Evaluation Presentations Folder
│   ├── README.md                                    # Presentations Index & Defense Notes
│   ├── Review_1_Requirements_and_ER_Design.pdf      # Review 1 (11 Slides) - PDF
│   ├── Review_1_Requirements_and_ER_Design.pptx     # Review 1 (11 Slides) - Editable PPTX
│   ├── Review_2_Normalization_and_SQL_Implementation.pdf # Review 2 (12 Slides) - PDF
│   ├── Review_2_Normalization_and_SQL_Implementation.pptx# Review 2 (12 Slides) - Editable PPTX
│   ├── Review_3_Final_Implementation_and_Demo.pdf   # Review 3 (12 Slides) - PDF
│   ├── Review_3_Final_Implementation_and_Demo.pptx  # Review 3 (12 Slides) - Editable PPTX
│   └── generate_presentations.py                    # Presentation Builder Script
├── docs/                                            # Academic Documentation & Assets
│   ├── Railway_Ticket_Reservation_DBMS_PBL_Report.docx
│   ├── Railway_Ticket_Reservation_DBMS_PBL_Report.pdf
│   ├── data_dictionary.md                           # Comprehensive Schema Data Dictionary
│   ├── functional_dependencies.md                   # Formal FDs & 3NF Normalization Proof
│   ├── test_results.md                              # 16/16 Test Execution Logs & Scenarios
│   ├── demo_script.md                               # Step-by-Step 5–8 Minute Oral Demo Script
│   ├── viva_qa.md                                   # 21 Viva Q&A + 5 Deep-Dive Defenses
│   └── screenshots/                                 # UI Screenshots & ER Diagram
└── Railway_Reservation_System/                      # Core Web Application & Database
    ├── app/
    │   ├── __init__.py                              # Flask Factory & SQLite PRAGMA FK hooks
    │   ├── config.py                                # Configuration (MySQL & SQLite fallback)
    │   ├── extensions.py                            # SQLAlchemy Database Instance
    │   ├── models/                                  # 14 SQLAlchemy Relational Models (3NF)
    │   ├── services/                                # Business Logic & Interval Math
    │   ├── routes/                                  # Flask Route Blueprints & Controllers
    │   └── templates/                               # Modern Responsive Jinja2 Templates
    ├── database/
    │   ├── schema.sql                               # MySQL 8.x InnoDB DDL (PK, FK, CHECK)
    │   ├── views.sql                                # Pre-Compiled Relational Views
    │   ├── reports.sql                              # 12 Benchmark SQL Query Scripts
    │   └── seed_data.py                             # Deterministic Dataset Seeder
    ├── tests/                                       # 16 Pytest Test Suites
    ├── requirements.txt                             # Python Dependencies
    └── run.py                                       # Startup Script & Auto-Seeder
```

---

## 10. Academic Deliverables & Course Artifacts

| Deliverable | Location | Description |
|---|---|---|
| **Official 40-Page Report** | [Report PDF](Railway_Ticket_Reservation_DBMS_PBL_Report.pdf) • [Word DOCX](Railway_Ticket_Reservation_DBMS_PBL_Report.docx) | Formal Woxsen University DBMS Project Report (strictly formatted to 40 pages) |
| **Review 1 Presentation** | [PDF](presentations/Review_1_Requirements_and_ER_Design.pdf) • [PPTX](presentations/Review_1_Requirements_and_ER_Design.pptx) | Week 7 (5 Marks): Requirements, Scope, Business Rules, ER Diagram |
| **Review 2 Presentation** | [PDF](presentations/Review_2_Normalization_and_SQL_Implementation.pdf) • [PPTX](presentations/Review_2_Normalization_and_SQL_Implementation.pptx) | Week 11 (5 Marks): 3NF Normalization, Functional Dependencies, DDL, SQL Queries |
| **Review 3 Presentation** | [PDF](presentations/Review_3_Final_Implementation_and_Demo.pdf) • [PPTX](presentations/Review_3_Final_Implementation_and_Demo.pptx) | Week 16 (5 Marks): Full System Demo, Screenshots, Concurrency, Pytest Evidence |
| **Relational Data Dictionary**| [docs/data_dictionary.md](docs/data_dictionary.md) | Attribute types, nullability, keys, default values, and domain constraints |
| **Normalization Proofs** | [docs/functional_dependencies.md](docs/functional_dependencies.md) | Candidate keys, FDs, and step-by-step 1NF/2NF/3NF decomposition proofs |
| **Viva Voce Defense Bank** | [docs/viva_qa.md](docs/viva_qa.md) | 21 Core Conceptual Viva Questions + 5 Deep-Dive Technical Defenses |
| **Live Demo Script** | [docs/demo_script.md](docs/demo_script.md) | Structured 5–8 minute oral presentation and workflow script for faculty review |
| **Automated Test Evidence** | [docs/test_results.md](docs/test_results.md) | Complete test descriptions and passed execution transcripts (16/16 tests) |

---

<div align="center">

**Developed with ❤️ by Heman (25WU0102097) — School of Technology, Woxsen University**

</div>
