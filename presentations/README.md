# Project Evaluation & Review Presentations

This directory contains the complete slide decks and documentation for all three formal academic reviews of the **Railway Ticket Reservation and Journey Management System**, developed for the **Database Management Systems (DBMS)** PBL curriculum at **School of Technology, Woxsen University**.

> **Author:** Heman (Roll No: `25WU0102097`)  
> **Program & Section:** B.Tech CSE (AIML) — AIML Rhinos  
> **Faculty Mentor:** Prof. Sahithi  
> **Academic Year:** 2026 – 2027  

---

## Quick Download & Online Viewing Index

| Review Milestone | Academic Weighting | Direct Online Preview (PDF) | Editable PowerPoint (PPTX) | Slide Count | Focus Area |
|---|---|---|---|---|---|
| **Review 1** | Week 7 (5 Marks) | [View Review 1 PDF](Review_1_Requirements_and_ER_Design.pdf) | [Download Review 1 PPTX](Review_1_Requirements_and_ER_Design.pptx) | 11 Slides | Problem Definition, Scope, Business Rules, ER Modeling & Cardinalities |
| **Review 2** | Week 11 (5 Marks) | [View Review 2 PDF](Review_2_Normalization_and_SQL_Implementation.pdf) | [Download Review 2 PPTX](Review_2_Normalization_and_SQL_Implementation.pptx) | 12 Slides | 3NF Normalization, Functional Dependencies, Relational Schema, DDL & 12 SQL Analytics |
| **Review 3** | Week 16 (5 Marks) | [View Review 3 PDF](Review_3_Final_Implementation_and_Demo.pdf) | [Download Review 3 PPTX](Review_3_Final_Implementation_and_Demo.pptx) | 12 Slides | Full-Stack Prototype, Interval Math, ACID Concurrency, Waitlist Engine, Live Demo |

---

## Detailed Slide Outlines

### Review 1: Requirements Definition, Scope & ER Modeling
**Focus:** Review-I focuses on domain decomposition, identifying enterprise entities, establishing relational cardinalities, and constructing the comprehensive Entity-Relationship Diagram (ERD).

- **Slide 1:** Title Slide (Institutional Affiliation, Student Roll Number, Faculty Guide)
- **Slide 2:** Problem Statement & Motivation (Railway multi-hop seat reuse vs point-to-point airline reservation)
- **Slide 3:** Project Scope, System Boundaries & Operational Assumptions
- **Slide 4:** Proposed Solution Strategy (Segment interval modeling, 3NF schema, pessimistic concurrency)
- **Slide 5:** Functional Requirements Matrix (Train search, reservation, waitlist queue, cancellation & refund)
- **Slide 6:** Non-Functional Requirements (ACID compliance, latency < 150ms, data integrity constraints)
- **Slide 7:** Comprehensive Entity-Relationship Diagram (ERD) Architecture (14 Relations)
- **Slide 8:** Entity Catalog & Key Attribute Specifications (Master vs Transactional tables)
- **Slide 9:** Cardinality Mapping & Relationship Multiplicity (Resolving M:N relationships)
- **Slide 10:** Review 1 Milestones & Deliverables Summary
- **Slide 11:** Technical Mentorship Alignment & Question Defense

---

### Review 2: Relational Schema, Normalization & SQL Queries
**Focus:** Review-II details the conversion of the approved conceptual ER model into a strict 3NF relational database schema, functional dependency validation, DDL constraints, and 12 analytical SQL queries.

- **Slide 1:** Title Slide & Project Identification
- **Slide 2:** Review 1 Recap & Action Items Addressed
- **Slide 3:** Relational Schema Transformation (14 Decoupled Relations)
- **Slide 4:** Functional Dependencies (FDs) and Minimal Candidate Key Derivation
- **Slide 5:** Step-by-Step Normalization Proof (1NF $\rightarrow$ 2NF $\rightarrow$ 3NF)
- **Slide 6:** Database Integrity Architecture (PKs, Composite FKs with Cascading, CHECK & UNIQUE Constraints)
- **Slide 7:** Relational Data Dictionary Specification
- **Slide 8:** Production DDL & MySQL 8.x InnoDB Architecture (`PRAGMA foreign_keys` for SQLite)
- **Slide 9:** Pre-Compiled Relational Views (`vw_confirmed_segments`, `vw_booking_summary`, `vw_train_occupancy_summary`)
- **Slide 10:** 12 Benchmark SQL Analytical Queries (Group by, Window Aggregations, Revenue Reconciliation)
- **Slide 11:** Synthetic Dataset Seeder & Automated Pytest Validation
- **Slide 12:** Review 2 Summary & Roadmap to Review 3

---

### Review 3: Full-Stack Implementation, Architecture & Live Demo
**Focus:** Review-III showcases the end-to-end working software prototype built on Python/Flask and SQLAlchemy, demonstrates the half-open interval seat allocation math, showcases concurrency safety, and executes test suites.

- **Slide 1:** Title Slide & Final Review Overview
- **Slide 2:** Full-Stack System Architecture (Flask Modular Blueprints, SQLAlchemy ORM, Jinja2 UI)
- **Slide 3:** Segment-Wise Half-Open Interval Seat Allocation Algorithm ($[s, e) \cap [start, end) \neq \emptyset$)
- **Slide 4:** Transaction Isolation & ACID Concurrency (Pessimistic Row Locking with `SELECT ... FOR UPDATE`)
- **Slide 5:** Dynamic Fare Calculation & Class Tariff Engine
- **Slide 6:** Cancellation Policy & Automated FIFO Waitlist Promotion Engine
- **Slide 7:** UI Walkthrough: Dashboard Analytics & Multi-Hop Station Search
- **Slide 8:** UI Walkthrough: Confirmed ERS Ticket Slip & Real-Time Waitlist Tracker
- **Slide 9:** UI Walkthrough: Executive SQL Analytics Console & Admin Schema Explorer
- **Slide 10:** Automated Test Suite Verification (16/16 Passed Pytest Suites)
- **Slide 11:** Limitations, Scalability Analysis & Future Engineering Roadmap
- **Slide 12:** Project Conclusion, Deliverables Handover & Viva Defense

---

## How to Regenerate Presentations

The presentations are automatically built using the Python automation script [generate_presentations.py](generate_presentations.py). To recompile or modify slide contents:

```bash
# 1. Activate project virtual environment
source ../venv/bin/activate

# 2. Re-run generator script
python generate_presentations.py

# 3. Export to PDF via LibreOffice (headless)
soffice --headless --convert-to pdf Review_1_Requirements_and_ER_Design.pptx
soffice --headless --convert-to pdf Review_2_Normalization_and_SQL_Implementation.pptx
soffice --headless --convert-to pdf Review_3_Final_Implementation_and_Demo.pptx
```
