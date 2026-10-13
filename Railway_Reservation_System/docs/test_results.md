# AUTOMATED TEST RESULTS AND VERIFICATION LOG
## Railway Ticket Reservation and Journey Management System
**Execution Date:** 2026-10-13  
**Test Framework:** pytest 8.4.2 | Python 3.9.6  
**Execution Environment:** macOS Darwin (arm64) | SQLite FK-Enforced Test Engine & MySQL InnoDB Dialect  
**Total Tests:** 16  
**Passed:** 16 (100%)  
**Failed:** 0 (0%)  
**Warnings:** 0  
**Execution Duration:** 0.36 seconds  

---

## 1. Test Execution Summary Table

| # | Test Case Identifier | Module | Category | Expected Outcome | Actual Outcome | Status |
|---|---|---|---|---|---|:---:|
| 1 | `test_interval_overlap_logic` | `test_availability.py` | Business Logic | $[1,2)$ does not overlap $[2,4)$; $[1,3)$ overlaps $[2,4)$ | Overlap formula evaluated correctly | **PASSED** |
| 2 | `test_non_overlapping_seat_reuse` | `test_availability.py` | Business Logic | Seat C1-1 is allocated on both [1,2) and [2,4) concurrently | Both allocations active in database | **PASSED** |
| 3 | `test_conflicting_interval_detection` | `test_availability.py` | Integrity | Request for [1,4) identifies Seat C1-1 as conflicting/occupied | Conflict detected, seat blocked | **PASSED** |
| 4 | `test_cancelled_allocation_restores_availability` | `test_availability.py` | State Machine | Cancelled segment on Seat C1-3 frees seat for reuse | Seat C1-3 is returned as available | **PASSED** |
| 5 | `test_eligible_cancellation_and_refund_policy` | `test_cancellations.py` | Financial Audit | 20% cancellation fee deducted, 80% refunded to passenger | Fee: ₹154.80, Refund: ₹619.20 | **PASSED** |
| 6 | `test_duplicate_cancellation_rejected` | `test_cancellations.py` | Transaction Safety| Second cancellation attempt on same booking raises ValueError | ValueError raised, duplicate blocked | **PASSED** |
| 7 | `test_automated_waitlist_promotion` | `test_cancellations.py` | Concurrency & Queue | Freeing confirmed seat promotes next waiting passenger atomically | Candidate promoted to CONFIRMED | **PASSED** |
| 8 | `test_unique_train_number_constraint` | `test_integrity.py` | DDL Constraints | Inserting duplicate train number raises IntegrityError | IntegrityError raised | **PASSED** |
| 9 | `test_invalid_foreign_key_rejected` | `test_integrity.py` | Referential Integrity| Referencing non-existent train_id raises IntegrityError | IntegrityError raised | **PASSED** |
| 10 | `test_passenger_age_check_constraint` | `test_integrity.py` | Domain Constraints | Passenger age > 120 rejected by CHECK constraint | IntegrityError raised | **PASSED** |
| 11 | `test_negative_fare_check_constraint` | `test_integrity.py` | Domain Constraints | Negative base_fare in FareRule rejected by CHECK constraint | IntegrityError raised | **PASSED** |
| 12 | `test_duplicate_stop_sequence_rejected` | `test_integrity.py` | DDL Constraints | Duplicate (route_id, stop_sequence) raises IntegrityError | IntegrityError raised | **PASSED** |
| 13 | `test_all_12_reports_execute_successfully` | `test_reports.py` | SQL Execution | All 12 benchmark SQL reports execute without syntax errors | All 12 returned non-empty records | **PASSED** |
| 14 | `test_valid_booking_success` | `test_reservations.py` | Transactions | Booking creates PNR, JourneySegment, and Payment atomically | All 3 records committed in DB | **PASSED** |
| 15 | `test_invalid_origin_dest_sequence_fails`| `test_reservations.py` | Validation | Booking backward journey (dest before origin) rejected | ValueError raised | **PASSED** |
| 16 | `test_train_runs_isolation` | `test_reservations.py` | Normalization | Bookings on same seat across different dates do not conflict | Both bookings confirmed on dates | **PASSED** |

---

## 2. Raw Pytest Execution Transcript

```text
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Users/heman08/Documents/dbms pbl/venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/heman08/Documents/dbms pbl
collecting ... collected 16 items

Railway_Reservation_System/tests/test_availability.py::test_interval_overlap_logic PASSED [  6%]
Railway_Reservation_System/tests/test_availability.py::test_non_overlapping_seat_reuse PASSED [ 12%]
Railway_Reservation_System/tests/test_availability.py::test_conflicting_interval_detection PASSED [ 18%]
Railway_Reservation_System/tests/test_availability.py::test_cancelled_allocation_restores_availability PASSED [ 25%]
Railway_Reservation_System/tests/test_cancellations.py::test_eligible_cancellation_and_refund_policy PASSED [ 31%]
Railway_Reservation_System/tests/test_cancellations.py::test_duplicate_cancellation_rejected PASSED [ 37%]
Railway_Reservation_System/tests/test_cancellations.py::test_automated_waitlist_promotion PASSED [ 43%]
Railway_Reservation_System/tests/test_integrity.py::test_unique_train_number_constraint PASSED [ 50%]
Railway_Reservation_System/tests/test_integrity.py::test_invalid_foreign_key_rejected PASSED [ 56%]
Railway_Reservation_System/tests/test_integrity.py::test_passenger_age_check_constraint PASSED [ 62%]
Railway_Reservation_System/tests/test_integrity.py::test_negative_fare_check_constraint PASSED [ 68%]
Railway_Reservation_System/tests/test_integrity.py::test_duplicate_stop_sequence_rejected PASSED [ 75%]
Railway_Reservation_System/tests/test_reports.py::test_all_12_reports_execute_successfully PASSED [ 81%]
Railway_Reservation_System/tests/test_reservations.py::test_valid_booking_success PASSED [ 87%]
Railway_Reservation_System/tests/test_reservations.py::test_invalid_origin_dest_sequence_fails PASSED [ 93%]
Railway_Reservation_System/tests/test_reservations.py::test_train_runs_isolation PASSED [100%]

============================== 16 passed in 0.36s ==============================
```
