# REPEATABLE 5–8 MINUTE LIVE DEMONSTRATION SCRIPT
## Railway Ticket Reservation and Journey Management System
**Academic Review Demonstration Guide**

---

### Step 1: Launch Application & Verify Dashboard
- **URL:** `http://127.0.0.1:5001/`
- **Actions:**
  1. Open the dashboard.
  2. Point out the live KPI cards: Active Trains (3), Registered Passengers (8), Confirmed Bookings (3), Waitlist Queue (1), Cancellations (1), and Net Retained Revenue (₹5,106.80).
  3. Show that all values are computed dynamically from the relational database via `SUM`, `COUNT`, and table joins rather than hardcoded.

---

### Step 2: Search Trains & Check Segment-Wise Seat Availability
- **URL:** `http://127.0.0.1:5001/search`
- **Actions:**
  1. Select **Origin:** `NDLS` (New Delhi).
  2. Select **Destination:** `BSB` (Varanasi Junction).
  3. Select **Date:** `2026-10-14`.
  4. Click **Find Trains**.
  5. Demonstrate the matching service: `22436 - Vande Bharat Express`.
  6. Point out the ordered stop sequences (NDLS is Stop #1, BSB is Stop #4, Distance: 755 km).
  7. Show class availability cards: AC Chair Car (CC) and First Class (1A) with deterministic fare calculations.

---

### Step 3: Book a Confirmed Ticket
- **Actions:**
  1. Click **Book Seat** under AC Chair Car (CC).
  2. Select a passenger profile (e.g., `Rajesh Kumar`).
  3. Choose preferred seat or retain auto-allocation.
  4. Point out the calculated fare breakdown (Base fare + distance charge + reservation fee).
  5. Click **Confirm Booking & Process Simulated Payment**.
  6. Show the generated Electronic Reservation Slip (ERS) with 10-digit PNR, assigned Coach & Seat number, and transaction reference.

---

### Step 4: Prove Segment-Wise Non-Overlapping Seat Reuse
- **Actions:**
  1. Open the database admin or inspection view (`/admin`).
  2. Explain the benchmark seed records:
     - Passenger 1 (Aarav Sharma) holds Seat `C1-1` on interval `[NDLS, CNB)` (Stop #1 to Stop #2).
     - Passenger 2 (Priya Patel) holds the **exact same** Seat `C1-1` on interval `[CNB, BSB)` (Stop #2 to Stop #4).
  3. Show how both reservations coexist actively in `journey_segments` because $[1, 2)$ and $[2, 4)$ do not overlap:
     $$\text{existing.start} < \text{req.end} \quad \text{AND} \quad \text{req.start} < \text{existing.end}$$
     $$1 < 4 \ (\text{True}) \quad \text{AND} \quad 2 < 2 \ (\text{False}) \implies \text{No Conflict!}$$
  4. Demonstrate that a conflicting request for interval `[NDLS, BSB)` $[1, 4)$ correctly blocks Seat `C1-1`.

---

### Step 5: Cancel a Booking & Show Automated Waitlist Promotion
- **URL:** `http://127.0.0.1:5001/cancel`
- **Actions:**
  1. Enter PNR for a confirmed passenger.
  2. View the **Cancellation Confirmation & Refund Preview** page.
  3. Point out the explicit policy enforcement: 20% cancellation deduction retained, 80% refunded to passenger.
  4. Click **Confirm Ticket Cancellation**.
  5. Show the notification confirming ticket cancellation, refund disbursement, and **automated promotion of the next eligible waitlisted passenger** onto the freed seat.
  6. Visit `/waitlist` to show the updated status changed from `WAITING` to `PROMOTED`.

---

### Step 6: Review SQL Reports Hub
- **URL:** `http://127.0.0.1:5001/reports`
- **Actions:**
  1. Walk the reviewer through Report 1 (Segment-Wise Availability Summary).
  2. Click Report 4 (Coach Occupancy Percentage).
  3. Click Report 9 (Financial Reconciliation Audit).
  4. Show how the database views and aggregate queries reconcile total fare, payments collected, cancellation fees retained, and net revenue.
