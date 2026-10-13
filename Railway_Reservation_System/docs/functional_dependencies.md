# FUNCTIONAL DEPENDENCIES AND NORMALIZATION PROOF
## Railway Ticket Reservation and Journey Management System
**Academic Course:** Database Management Systems (B.Tech Computer Science & Engineering)  
**Standard:** Codd's Relational Normal Forms (1NF, 2NF, 3NF)

---

## 1. Candidate Keys and Functional Dependencies (FD) Inventory

For each relation in the schema, the minimal candidate keys and non-trivial functional dependencies are formally specified below.

### 1. `stations`
- **Candidate Keys:** `{station_id}`, `{station_code}`
- **Selected Primary Key:** `station_id`
- **Functional Dependencies:**
  - $FD_1: \text{station\_id} \rightarrow \{\text{station\_code}, \text{station\_name}, \text{city}, \text{state}\}$
  - $FD_2: \text{station\_code} \rightarrow \{\text{station\_id}, \text{station\_name}, \text{city}, \text{state}\}$

### 2. `routes`
- **Candidate Keys:** `{route_id}`, `{route_code}`
- **Selected Primary Key:** `route_id`
- **Functional Dependencies:**
  - $FD_1: \text{route\_id} \rightarrow \{\text{route\_code}, \text{source\_station\_id}, \text{destination\_station\_id}, \text{total\_distance\_km}\}$
  - $FD_2: \text{route\_code} \rightarrow \{\text{route\_id}, \text{source\_station\_id}, \text{destination\_station\_id}, \text{total\_distance\_km}\}$

### 3. `train_stops`
- **Candidate Keys:** `{stop_id}`, `{route_id, stop_sequence}`, `{route_id, station_id}`
- **Selected Primary Key:** `stop_id`
- **Functional Dependencies:**
  - $FD_1: \text{stop\_id} \rightarrow \{\text{route\_id}, \text{station\_id}, \text{stop\_sequence}, \text{distance\_from\_source\_km}, \text{arrival\_time}, \text{departure\_time}\}$
  - $FD_2: \{\text{route\_id}, \text{stop\_sequence}\} \rightarrow \{\text{stop\_id}, \text{station\_id}, \text{distance\_from\_source\_km}, \text{arrival\_time}, \text{departure\_time}\}$
  - $FD_3: \{\text{route\_id}, \text{station\_id}\} \rightarrow \{\text{stop\_id}, \text{stop\_sequence}, \text{distance\_from\_source\_km}, \text{arrival\_time}, \text{departure\_time}\}$

### 4. `trains`
- **Candidate Keys:** `{train_id}`, `{train_number}`
- **Selected Primary Key:** `train_id`
- **Functional Dependencies:**
  - $FD_1: \text{train\_id} \rightarrow \{\text{train\_number}, \text{train\_name}, \text{train\_type}, \text{route\_id}\}$
  - $FD_2: \text{train\_number} \rightarrow \{\text{train\_id}, \text{train\_name}, \text{train\_type}, \text{route\_id}\}$

### 5. `train_runs`
- **Candidate Keys:** `{run_id}`, `{train_id, run_date}`
- **Selected Primary Key:** `run_id`
- **Functional Dependencies:**
  - $FD_1: \text{run\_id} \rightarrow \{\text{train\_id}, \text{run\_date}, \text{status}\}$
  - $FD_2: \{\text{train\_id}, \text{run\_date}\} \rightarrow \{\text{run\_id}, \text{status}\}$

### 6. `coaches`
- **Candidate Keys:** `{coach_id}`, `{train_id, coach_code}`
- **Selected Primary Key:** `coach_id`
- **Functional Dependencies:**
  - $FD_1: \text{coach\_id} \rightarrow \{\text{train\_id}, \text{coach\_code}, \text{travel\_class}, \text{total\_seats}\}$
  - $FD_2: \{\text{train\_id}, \text{coach\_code}\} \rightarrow \{\text{coach\_id}, \text{travel\_class}, \text{total\_seats}\}$

### 7. `seats`
- **Candidate Keys:** `{seat_id}`, `{coach_id, seat_number}`
- **Selected Primary Key:** `seat_id`
- **Functional Dependencies:**
  - $FD_1: \text{seat\_id} \rightarrow \{\text{coach\_id}, \text{seat\_number}, \text{berth\_type}\}$
  - $FD_2: \{\text{coach\_id}, \text{seat\_number}\} \rightarrow \{\text{seat\_id}, \text{berth\_type}\}$

### 8. `passengers`
- **Candidate Keys:** `{passenger_id}`, `{email}`, `{id_card_type, id_card_number}`
- **Selected Primary Key:** `passenger_id`
- **Functional Dependencies:**
  - $FD_1: \text{passenger\_id} \rightarrow \{\text{full\_name}, \text{gender}, \text{age}, \text{email}, \text{phone}, \text{id\_card\_type}, \text{id\_card\_number}\}$
  - $FD_2: \text{email} \rightarrow \{\text{passenger\_id}, \text{full\_name}, \text{gender}, \text{age}, \text{phone}, \text{id\_card\_type}, \text{id\_card\_number}\}$

### 9. `fare_rules`
- **Candidate Keys:** `{fare_id}`, `{train_type, travel_class}`
- **Selected Primary Key:** `fare_id`
- **Functional Dependencies:**
  - $FD_1: \text{fare\_id} \rightarrow \{\text{train\_type}, \text{travel\_class}, \text{base\_fare}, \text{rate\_per\_km}, \text{reservation\_fee}\}$
  - $FD_2: \{\text{train\_type}, \text{travel\_class}\} \rightarrow \{\text{fare\_id}, \text{base\_fare}, \text{rate\_per\_km}, \text{reservation\_fee}\}$

### 10. `bookings`
- **Candidate Keys:** `{booking_id}`, `{pnr_number}`
- **Selected Primary Key:** `booking_id`
- **Functional Dependencies:**
  - $FD_1: \text{booking\_id} \rightarrow \{\text{pnr\_number}, \text{run\_id}, \text{passenger\_id}, \text{origin\_station\_id}, \text{destination\_station\_id}, \text{origin\_stop\_seq}, \text{destination\_stop\_seq}, \text{travel\_class}, \text{booking\_status}, \text{total\_fare}, \text{booked\_at}\}$
  - $FD_2: \text{pnr\_number} \rightarrow \{\text{booking\_id}, \text{run\_id}, \text{passenger\_id}, \text{origin\_station\_id}, \text{destination\_station\_id}, \text{origin\_stop\_seq}, \text{destination\_stop\_seq}, \text{travel\_class}, \text{booking\_status}, \text{total\_fare}, \text{booked\_at}\}$

### 11. `journey_segments`
- **Candidate Keys:** `{segment_id}`
- **Selected Primary Key:** `segment_id`
- **Functional Dependencies:**
  - $FD_1: \text{segment\_id} \rightarrow \{\text{booking\_id}, \text{seat\_id}, \text{run\_id}, \text{start\_stop\_seq}, \text{end\_stop\_seq}, \text{allocation\_status}\}$

### 12. `waitlists`
- **Candidate Keys:** `{waitlist_id}`
- **Selected Primary Key:** `waitlist_id`
- **Functional Dependencies:**
  - $FD_1: \text{waitlist\_id} \rightarrow \{\text{booking\_id}, \text{run\_id}, \text{travel\_class}, \text{origin\_stop\_seq}, \text{destination\_stop\_seq}, \text{position}, \text{waitlist\_status}, \text{created\_at}\}$

### 13. `payments`
- **Candidate Keys:** `{payment_id}`, `{transaction_reference}`
- **Selected Primary Key:** `payment_id`
- **Functional Dependencies:**
  - $FD_1: \text{payment\_id} \rightarrow \{\text{booking\_id}, \text{amount}, \text{payment\_method}, \text{transaction\_reference}, \text{payment\_status}, \text{paid\_at}\}$
  - $FD_2: \text{transaction\_reference} \rightarrow \{\text{payment\_id}, \text{booking\_id}, \text{amount}, \text{payment\_method}, \text{payment\_status}, \text{paid\_at}\}$

### 14. `cancellations`
- **Candidate Keys:** `{cancellation_id}`, `{booking_id}`
- **Selected Primary Key:** `cancellation_id`
- **Functional Dependencies:**
  - $FD_1: \text{cancellation\_id} \rightarrow \{\text{booking\_id}, \text{cancellation\_reason}, \text{cancellation\_fee}, \text{refund\_amount}, \text{refund\_status}, \text{cancelled\_at}\}$
  - $FD_2: \text{booking\_id} \rightarrow \{\text{cancellation\_id}, \text{cancellation\_reason}, \text{cancellation\_fee}, \text{refund\_amount}, \text{refund\_status}, \text{cancelled\_at}\}$

---

## 2. Step-by-Step Normalization Walkthrough

### Unnormalized Form (UNF)
Consider a naive reservation spreadsheet record:
`RESERVATION_UNF(PNR, PassengerName, PassengerAge, PassengerEmail, TrainNum, TrainName, TrainType, RunDate, RouteStops, CoachCode, SeatNum, BerthType, OriginStn, DestStn, Fare, PaymentRef, CancelReason, RefundAmt)`

**Problems with UNF:**
1. Multivalued attribute `RouteStops` (contains comma-separated station codes and arrival times).
2. Repeating groups of passenger records and segment stops.
3. Massive data redundancy across train runs and passengers.

---

### First Normal Form (1NF)
**Rule:** Every attribute must contain only atomic (indivisible) values, and there must be no repeating groups or multivalued columns.

**Decomposition to 1NF:**
1. Split `RouteStops` into individual ordered tuple records `(route_id, stop_sequence, station_id, arrival_time, departure_time)`.
2. Ensure each passenger profile, booking, and seat is represented as a single discrete row.
3. Establish unique primary keys for every record.

**Resulting 1NF Relations:**
- Atomic values achieved.
- Composite primary key candidate in booking: `{PNR, PassengerID, TrainNum, RunDate, CoachCode, SeatNum}`.

---

### Second Normal Form (2NF)
**Rule:** Must be in 1NF, and no non-prime attribute may be partially dependent on any proper subset of a composite candidate key (No Partial Dependencies).

**Identified Partial Dependencies in 1NF:**
- On composite key `{TrainNum, RunDate, CoachCode, SeatNum}`:
  - $\text{TrainNum} \rightarrow \{\text{TrainName}, \text{TrainType}\}$ *(Partially depends on TrainNum only)*
  - $\text{CoachCode} \rightarrow \text{TravelClass}$ *(Partially depends on CoachCode only)*
  - $\text{SeatNum} \rightarrow \text{BerthType}$ *(Partially depends on Coach and Seat only)*
  - $\text{PassengerID} \rightarrow \{\text{PassengerName}, \text{PassengerAge}, \text{PassengerEmail}\}$ *(Partially depends on PassengerID only)*

**Decomposition to 2NF:**
1. Isolate `Train` catalog from `TrainRun`:
   - `TRAIN(TrainID, TrainNumber, TrainName, TrainType, RouteID)`
   - `TRAIN_RUN(RunID, TrainID, RunDate, Status)`
2. Isolate `Coach` and `Seat`:
   - `COACH(CoachID, TrainID, CoachCode, TravelClass, TotalSeats)`
   - `SEAT(SeatID, CoachID, SeatNumber, BerthType)`
3. Isolate `Passenger`:
   - `PASSENGER(PassengerID, FullName, Gender, Age, Email, Phone, IDCardType, IDCardNumber)`

Now, every non-key attribute depends entirely on the whole candidate key of its respective table.

---

### Third Normal Form (3NF)
**Rule:** Must be in 2NF, and no non-prime attribute may be transitively dependent on a candidate key (No Transitive Dependencies: $X \rightarrow Y$ and $Y \rightarrow Z$, where $Y$ is not a superkey).

**Identified Transitive Dependencies in 2NF:**
1. In `BOOKING`:
   - $\text{BookingID} \rightarrow \text{PaymentRef} \rightarrow \{\text{Amount}, \text{PaymentMethod}, \text{PaymentStatus}\}$
   - $\text{BookingID} \rightarrow \text{CancellationID} \rightarrow \{\text{CancelReason}, \text{CancelFee}, \text{RefundAmt}\}$
   - $\text{BookingID} \rightarrow \{\text{TrainType}, \text{TravelClass}\} \rightarrow \{\text{BaseFare}, \text{RatePerKm}\}$
2. In `TRAIN`:
   - $\text{TrainID} \rightarrow \text{RouteID} \rightarrow \{\text{SourceStation}, \text{DestStation}, \text{Distance}\}$

**Decomposition to 3NF:**
1. Extract `FareRule` table:
   - `FARE_RULE(FareID, TrainType, TravelClass, BaseFare, RatePerKm, ReservationFee)`
2. Extract `Payment` table:
   - `PAYMENT(PaymentID, BookingID, Amount, PaymentMethod, TransactionReference, PaymentStatus, PaidAt)`
3. Extract `Cancellation` table:
   - `CANCELLATION(CancellationID, BookingID, CancellationReason, CancellationFee, RefundAmount, RefundStatus, CancelledAt)`
4. Extract `Route` and `TrainStop` tables:
   - `ROUTE(RouteID, RouteCode, SourceStationID, DestinationStationID, TotalDistanceKm)`
   - `TRAIN_STOP(StopID, RouteID, StationID, StopSequence, DistanceFromSourceKm, ArrivalTime, DepartureTime)`
5. Extract `JourneySegment`:
   - `JOURNEY_SEGMENT(SegmentID, BookingID, SeatID, RunID, StartStopSeq, EndStopSeq, AllocationStatus)`

---

## 3. Anomaly Prevention Summary

| Anomaly Type | Problem in Unnormalized Design | Resolution in 3NF Design |
|---|---|---|
| **Insertion Anomaly** | Cannot create a new train or route without booking a passenger on it. | `trains`, `routes`, and `stations` exist independently; trains can be configured without passengers. |
| **Deletion Anomaly** | Deleting a passenger cancels the entire train schedule and station records. | Deleting or cancelling a booking only affects `bookings` and `cancellations`; station and train catalog records remain completely intact. |
| **Update Anomaly** | Changing train name requires updating every historical booking row for that train. | Train name is updated in exactly one row in the `trains` table, automatically reflected across all historical runs. |
