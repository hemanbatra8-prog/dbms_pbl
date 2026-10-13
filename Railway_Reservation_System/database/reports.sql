-- =====================================================================
-- RAILWAY RESERVATION SYSTEM - BENCHMARK SQL REPORTS
-- Demonstrating Joins, Nested Queries, Aggregations, HAVING, and Views
-- =====================================================================

-- REPORT 1: Segment-Wise Seat Availability by Train Run & Class (Aggregations + Multiple Joins)
SELECT 
    tr.run_id,
    t.train_number,
    t.train_name,
    tr.run_date,
    c.travel_class,
    COUNT(DISTINCT s.seat_id) AS total_class_seats,
    COUNT(DISTINCT js.segment_id) AS active_allocations,
    (COUNT(DISTINCT s.seat_id) - COUNT(DISTINCT js.seat_id)) AS unallocated_full_seats
FROM train_runs tr
JOIN trains t ON tr.train_id = t.train_id
JOIN coaches c ON t.train_id = c.train_id
JOIN seats s ON c.coach_id = s.coach_id
LEFT JOIN journey_segments js ON s.seat_id = js.seat_id 
    AND js.run_id = tr.run_id 
    AND js.allocation_status = 'ACTIVE'
GROUP BY tr.run_id, t.train_number, t.train_name, tr.run_date, c.travel_class
ORDER BY tr.run_date, t.train_number, c.travel_class;

-- REPORT 2: Passenger Booking History & Detailed Itinerary (Inner Joins + Date Formatting)
SELECT 
    b.pnr_number,
    p.full_name AS passenger_name,
    t.train_number,
    t.train_name,
    tr.run_date,
    b.travel_class,
    b.booking_status,
    b.total_fare,
    b.booked_at
FROM bookings b
JOIN passengers p ON b.passenger_id = p.passenger_id
JOIN train_runs tr ON b.run_id = tr.run_id
JOIN trains t ON tr.train_id = t.train_id
ORDER BY b.booked_at DESC;

-- REPORT 3: Active Waitlist Queue Priority and Waiting Position
SELECT 
    w.waitlist_id,
    w.position AS queue_position,
    w.waitlist_status,
    b.pnr_number,
    p.full_name AS passenger_name,
    t.train_number,
    tr.run_date,
    w.travel_class,
    w.created_at
FROM waitlists w
JOIN bookings b ON w.booking_id = b.booking_id
JOIN passengers p ON b.passenger_id = p.passenger_id
JOIN train_runs tr ON w.run_id = tr.run_id
JOIN trains t ON tr.train_id = t.train_id
ORDER BY tr.run_date, w.travel_class, w.position ASC;

-- REPORT 4: Coach Occupancy Percentage (Aggregation + Computed Metric)
SELECT 
    c.coach_id,
    t.train_number,
    c.coach_code,
    c.travel_class,
    c.total_seats,
    COUNT(DISTINCT js.segment_id) AS active_occupied_seats,
    ROUND((COUNT(DISTINCT js.segment_id) * 100.0 / c.total_seats), 2) AS occupancy_percentage
FROM coaches c
JOIN trains t ON c.train_id = t.train_id
JOIN seats s ON c.coach_id = s.coach_id
LEFT JOIN journey_segments js ON s.seat_id = js.seat_id AND js.allocation_status = 'ACTIVE'
GROUP BY c.coach_id, t.train_number, c.coach_code, c.travel_class, c.total_seats
ORDER BY t.train_number, c.coach_code;

-- REPORT 5: Route Demand and Passenger Volume Analysis (Multi-table Joins + SUM + COUNT)
SELECT 
    r.route_code,
    s_src.station_name AS origin_station,
    s_dst.station_name AS destination_station,
    r.total_distance_km,
    COUNT(b.booking_id) AS total_bookings,
    COALESCE(SUM(b.total_fare), 0) AS total_route_revenue
FROM routes r
JOIN stations s_src ON r.source_station_id = s_src.station_id
JOIN stations s_dst ON r.destination_station_id = s_dst.station_id
LEFT JOIN trains t ON r.route_id = t.route_id
LEFT JOIN train_runs tr ON t.train_id = tr.train_id
LEFT JOIN bookings b ON tr.run_id = b.run_id
GROUP BY r.route_id, r.route_code, s_src.station_name, s_dst.station_name, r.total_distance_km
ORDER BY total_bookings DESC;

-- REPORT 6: Cancellation Counts, Cancellation Fees, and Total Refund Disbursed
SELECT 
    c.cancellation_id,
    b.pnr_number,
    p.full_name AS passenger_name,
    c.cancellation_reason,
    c.cancellation_fee,
    c.refund_amount,
    c.refund_status,
    c.cancelled_at
FROM cancellations c
JOIN bookings b ON c.booking_id = b.booking_id
JOIN passengers p ON b.passenger_id = p.passenger_id
ORDER BY c.cancelled_at DESC;

-- REPORT 7: Passenger Complete Journey Details with Stations and Times
SELECT 
    b.pnr_number,
    p.full_name AS passenger_name,
    t.train_number,
    t.train_name,
    tr.run_date,
    s_orig.station_name AS boarding_station,
    ts_orig.departure_time,
    s_dest.station_name AS deboarding_station,
    ts_dest.arrival_time,
    b.travel_class,
    b.booking_status
FROM bookings b
JOIN passengers p ON b.passenger_id = p.passenger_id
JOIN train_runs tr ON b.run_id = tr.run_id
JOIN trains t ON tr.train_id = t.train_id
JOIN stations s_orig ON b.origin_station_id = s_orig.station_id
JOIN stations s_dest ON b.destination_station_id = s_dest.station_id
JOIN train_stops ts_orig ON t.route_id = ts_orig.route_id AND ts_orig.station_id = b.origin_station_id
JOIN train_stops ts_dest ON t.route_id = ts_dest.route_id AND ts_dest.station_id = b.destination_station_id
ORDER BY tr.run_date DESC, b.booking_id DESC;

-- REPORT 8: Revenue Grouped by Train and Travel Class (Excluding Cancelled Bookings)
SELECT 
    t.train_number,
    t.train_name,
    b.travel_class,
    COUNT(b.booking_id) AS ticket_count,
    SUM(b.total_fare) AS gross_revenue
FROM bookings b
JOIN train_runs tr ON b.run_id = tr.run_id
JOIN trains t ON tr.train_id = t.train_id
WHERE b.booking_status != 'CANCELLED'
GROUP BY t.train_number, t.train_name, b.travel_class
ORDER BY gross_revenue DESC;

-- REPORT 9: Booking and Payment Financial Reconciliation Audit
SELECT 
    (SELECT COALESCE(SUM(total_fare), 0) FROM bookings) AS total_gross_booking_fare,
    (SELECT COALESCE(SUM(amount), 0) FROM payments WHERE payment_status IN ('COMPLETED', 'REFUNDED')) AS total_payments_collected,
    (SELECT COALESCE(SUM(refund_amount), 0) FROM cancellations) AS total_refunds_disbursed,
    (SELECT COALESCE(SUM(cancellation_fee), 0) FROM cancellations) AS total_cancellation_charges_retained,
    ((SELECT COALESCE(SUM(amount), 0) FROM payments WHERE payment_status = 'COMPLETED') - 
     (SELECT COALESCE(SUM(refund_amount), 0) FROM cancellations)) AS net_company_revenue;

-- REPORT 10: Confirmed vs Waitlisted vs Cancelled Proportion Report
SELECT 
    booking_status,
    COUNT(*) AS booking_count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bookings)), 2) AS percentage_of_total
FROM bookings
GROUP BY booking_status;

-- REPORT 11: Route Stop Timetable & Distance Analysis
SELECT 
    t.train_number,
    t.train_name,
    r.route_code,
    ts.stop_sequence,
    st.station_code,
    st.station_name,
    ts.distance_from_source_km,
    ts.arrival_time,
    ts.departure_time
FROM train_stops ts
JOIN stations st ON ts.station_id = st.station_id
JOIN routes r ON ts.route_id = r.route_id
JOIN trains t ON r.route_id = t.route_id
ORDER BY t.train_number, ts.stop_sequence;

-- REPORT 12: High-Value Frequent Passengers (Nested Query + HAVING Clause)
SELECT 
    p.passenger_id,
    p.full_name,
    p.email,
    COUNT(b.booking_id) AS total_bookings,
    SUM(b.total_fare) AS total_spent
FROM passengers p
JOIN bookings b ON p.passenger_id = b.passenger_id
GROUP BY p.passenger_id, p.full_name, p.email
HAVING COUNT(b.booking_id) > 0
ORDER BY total_spent DESC;
