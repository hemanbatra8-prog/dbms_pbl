-- =====================================================================
-- DATABASE VIEWS
-- Relational Database Views for Operational Analytics and Reporting
-- =====================================================================

-- View 1: Active Confirmed Seat Allocations with Station and Train details
CREATE OR REPLACE VIEW vw_confirmed_segments AS
SELECT 
    js.segment_id,
    b.pnr_number,
    p.full_name AS passenger_name,
    t.train_number,
    t.train_name,
    tr.run_date,
    c.coach_code,
    c.travel_class,
    s.seat_number,
    s.berth_type,
    js.start_stop_seq,
    js.end_stop_seq,
    st_orig.station_code AS origin_station,
    st_dest.station_code AS dest_station
FROM journey_segments js
JOIN bookings b ON js.booking_id = b.booking_id
JOIN passengers p ON b.passenger_id = p.passenger_id
JOIN seats s ON js.seat_id = s.seat_id
JOIN coaches c ON s.coach_id = c.coach_id
JOIN train_runs tr ON js.run_id = tr.run_id
JOIN trains t ON tr.train_id = t.train_id
JOIN stations st_orig ON b.origin_station_id = st_orig.station_id
JOIN stations st_dest ON b.destination_station_id = st_dest.station_id
WHERE js.allocation_status = 'ACTIVE';

-- View 2: Booking Summary with Financial and Allocation Status
CREATE OR REPLACE VIEW vw_booking_summary AS
SELECT 
    b.booking_id,
    b.pnr_number,
    p.full_name AS passenger_name,
    t.train_number,
    t.train_name,
    tr.run_date,
    b.travel_class,
    b.booking_status,
    b.total_fare,
    pay.payment_status,
    pay.transaction_reference,
    canc.refund_amount,
    canc.cancellation_fee
FROM bookings b
JOIN passengers p ON b.passenger_id = p.passenger_id
JOIN train_runs tr ON b.run_id = tr.run_id
JOIN trains t ON tr.train_id = t.train_id
LEFT JOIN payments pay ON b.booking_id = pay.booking_id
LEFT JOIN cancellations canc ON b.booking_id = canc.booking_id;

-- View 3: Train Occupancy Summary
CREATE OR REPLACE VIEW vw_train_occupancy_summary AS
SELECT 
    tr.run_id,
    t.train_number,
    t.train_name,
    tr.run_date,
    COUNT(DISTINCT s.seat_id) AS total_physical_seats,
    COUNT(DISTINCT js.seat_id) AS occupied_seats_count,
    ROUND((COUNT(DISTINCT js.seat_id) * 100.0 / COUNT(DISTINCT s.seat_id)), 2) AS occupancy_ratio
FROM train_runs tr
JOIN trains t ON tr.train_id = t.train_id
JOIN coaches c ON t.train_id = c.train_id
JOIN seats s ON c.coach_id = s.coach_id
LEFT JOIN journey_segments js ON s.seat_id = js.seat_id 
    AND js.run_id = tr.run_id 
    AND js.allocation_status = 'ACTIVE'
GROUP BY tr.run_id, t.train_number, t.train_name, tr.run_date;

-- View 4: Station Timetable Schedule
CREATE OR REPLACE VIEW vw_station_timetable AS
SELECT 
    st.station_code,
    st.station_name,
    t.train_number,
    t.train_name,
    r.route_code,
    ts.stop_sequence,
    ts.arrival_time,
    ts.departure_time,
    ts.distance_from_source_km
FROM train_stops ts
JOIN stations st ON ts.station_id = st.station_id
JOIN routes r ON ts.route_id = r.route_id
JOIN trains t ON r.route_id = t.route_id
ORDER BY st.station_code, ts.arrival_time;
