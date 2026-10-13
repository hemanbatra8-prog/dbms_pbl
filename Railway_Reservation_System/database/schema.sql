-- =====================================================================
-- RAILWAY TICKET RESERVATION AND JOURNEY MANAGEMENT SYSTEM
-- Relational Database Schema DDL (MySQL 8.x / InnoDB)
-- Third Normal Form (3NF) Compliant
-- =====================================================================

SET FOREIGN_KEY_CHECKS = 0;

-- 1. STATIONS TABLE
DROP TABLE IF EXISTS stations;
CREATE TABLE stations (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_code VARCHAR(10) NOT NULL UNIQUE,
    station_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    INDEX idx_station_code (station_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. ROUTES TABLE
DROP TABLE IF EXISTS routes;
CREATE TABLE routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    route_code VARCHAR(30) NOT NULL UNIQUE,
    source_station_id INT NOT NULL,
    destination_station_id INT NOT NULL,
    total_distance_km DECIMAL(7, 2) NOT NULL,
    CONSTRAINT fk_route_source FOREIGN KEY (source_station_id) REFERENCES stations(station_id) ON DELETE RESTRICT,
    CONSTRAINT fk_route_dest FOREIGN KEY (destination_station_id) REFERENCES stations(station_id) ON DELETE RESTRICT,
    CONSTRAINT chk_route_distance CHECK (total_distance_km > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. TRAIN STOPS TABLE (Ordered station sequence along a route)
DROP TABLE IF EXISTS train_stops;
CREATE TABLE train_stops (
    stop_id INT AUTO_INCREMENT PRIMARY KEY,
    route_id INT NOT NULL,
    station_id INT NOT NULL,
    stop_sequence INT NOT NULL,
    distance_from_source_km DECIMAL(7, 2) NOT NULL,
    arrival_time TIME NULL,
    departure_time TIME NULL,
    CONSTRAINT fk_stop_route FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE,
    CONSTRAINT fk_stop_station FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE RESTRICT,
    CONSTRAINT uq_route_stop_seq UNIQUE (route_id, stop_sequence),
    CONSTRAINT uq_route_station UNIQUE (route_id, station_id),
    CONSTRAINT chk_stop_seq_positive CHECK (stop_sequence > 0),
    CONSTRAINT chk_stop_dist_nonneg CHECK (distance_from_source_km >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. TRAINS TABLE (Train catalog definition)
DROP TABLE IF EXISTS trains;
CREATE TABLE trains (
    train_id INT AUTO_INCREMENT PRIMARY KEY,
    train_number VARCHAR(10) NOT NULL UNIQUE,
    train_name VARCHAR(100) NOT NULL,
    train_type VARCHAR(30) NOT NULL,
    route_id INT NOT NULL,
    CONSTRAINT fk_train_route FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE RESTRICT,
    INDEX idx_train_number (train_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. TRAIN RUNS (SCHEDULES) TABLE (Dated operational train run instances)
DROP TABLE IF EXISTS train_runs;
CREATE TABLE train_runs (
    run_id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT NOT NULL,
    run_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    CONSTRAINT fk_run_train FOREIGN KEY (train_id) REFERENCES trains(train_id) ON DELETE CASCADE,
    CONSTRAINT uq_train_run_date UNIQUE (train_id, run_date),
    INDEX idx_run_date (run_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. COACHES TABLE
DROP TABLE IF EXISTS coaches;
CREATE TABLE coaches (
    coach_id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT NOT NULL,
    coach_code VARCHAR(10) NOT NULL,
    travel_class VARCHAR(10) NOT NULL,
    total_seats INT NOT NULL DEFAULT 72,
    CONSTRAINT fk_coach_train FOREIGN KEY (train_id) REFERENCES trains(train_id) ON DELETE CASCADE,
    CONSTRAINT uq_train_coach UNIQUE (train_id, coach_code),
    CONSTRAINT chk_coach_seats_pos CHECK (total_seats > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. SEATS TABLE
DROP TABLE IF EXISTS seats;
CREATE TABLE seats (
    seat_id INT AUTO_INCREMENT PRIMARY KEY,
    coach_id INT NOT NULL,
    seat_number INT NOT NULL,
    berth_type VARCHAR(15) NOT NULL,
    CONSTRAINT fk_seat_coach FOREIGN KEY (coach_id) REFERENCES coaches(coach_id) ON DELETE CASCADE,
    CONSTRAINT uq_coach_seat_number UNIQUE (coach_id, seat_number),
    CONSTRAINT chk_seat_num_positive CHECK (seat_number > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. PASSENGERS TABLE
DROP TABLE IF EXISTS passengers;
CREATE TABLE passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    id_card_type VARCHAR(20) NOT NULL,
    id_card_number VARCHAR(50) NOT NULL,
    CONSTRAINT chk_passenger_age CHECK (age > 0 AND age < 120),
    INDEX idx_passenger_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. FARE RULES TABLE
DROP TABLE IF EXISTS fare_rules;
CREATE TABLE fare_rules (
    fare_id INT AUTO_INCREMENT PRIMARY KEY,
    train_type VARCHAR(30) NOT NULL,
    travel_class VARCHAR(10) NOT NULL,
    base_fare DECIMAL(10, 2) NOT NULL,
    rate_per_km DECIMAL(6, 2) NOT NULL,
    reservation_fee DECIMAL(6, 2) NOT NULL DEFAULT 40.00,
    CONSTRAINT uq_train_type_class UNIQUE (train_type, travel_class),
    CONSTRAINT chk_base_fare_nonneg CHECK (base_fare >= 0),
    CONSTRAINT chk_rate_km_nonneg CHECK (rate_per_km >= 0),
    CONSTRAINT chk_res_fee_nonneg CHECK (reservation_fee >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. BOOKINGS TABLE
DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    pnr_number VARCHAR(12) NOT NULL UNIQUE,
    run_id INT NOT NULL,
    passenger_id INT NOT NULL,
    origin_station_id INT NOT NULL,
    destination_station_id INT NOT NULL,
    origin_stop_seq INT NOT NULL,
    destination_stop_seq INT NOT NULL,
    travel_class VARCHAR(10) NOT NULL,
    booking_status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    total_fare DECIMAL(10, 2) NOT NULL,
    booked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_booking_run FOREIGN KEY (run_id) REFERENCES train_runs(run_id) ON DELETE RESTRICT,
    CONSTRAINT fk_booking_passenger FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE RESTRICT,
    CONSTRAINT fk_booking_origin FOREIGN KEY (origin_station_id) REFERENCES stations(station_id) ON DELETE RESTRICT,
    CONSTRAINT fk_booking_dest FOREIGN KEY (destination_station_id) REFERENCES stations(station_id) ON DELETE RESTRICT,
    CONSTRAINT chk_booking_stop_order CHECK (destination_stop_seq > origin_stop_seq),
    CONSTRAINT chk_booking_fare_nonneg CHECK (total_fare >= 0),
    INDEX idx_booking_pnr (pnr_number),
    INDEX idx_booking_status (booking_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. JOURNEY SEGMENTS TABLE (Seat allocation over half-open interval [start_stop_seq, end_stop_seq))
DROP TABLE IF EXISTS journey_segments;
CREATE TABLE journey_segments (
    segment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    seat_id INT NOT NULL,
    run_id INT NOT NULL,
    start_stop_seq INT NOT NULL,
    end_stop_seq INT NOT NULL,
    allocation_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    CONSTRAINT fk_seg_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    CONSTRAINT fk_seg_seat FOREIGN KEY (seat_id) REFERENCES seats(seat_id) ON DELETE RESTRICT,
    CONSTRAINT fk_seg_run FOREIGN KEY (run_id) REFERENCES train_runs(run_id) ON DELETE CASCADE,
    CONSTRAINT chk_seg_seq_order CHECK (end_stop_seq > start_stop_seq),
    INDEX idx_seat_run_alloc (run_id, seat_id, allocation_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. WAITLIST TABLE
DROP TABLE IF EXISTS waitlists;
CREATE TABLE waitlists (
    waitlist_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    run_id INT NOT NULL,
    travel_class VARCHAR(10) NOT NULL,
    origin_stop_seq INT NOT NULL,
    destination_stop_seq INT NOT NULL,
    position INT NOT NULL,
    waitlist_status VARCHAR(20) NOT NULL DEFAULT 'WAITING',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_wl_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    CONSTRAINT fk_wl_run FOREIGN KEY (run_id) REFERENCES train_runs(run_id) ON DELETE CASCADE,
    CONSTRAINT chk_wl_pos_positive CHECK (position > 0),
    CONSTRAINT chk_wl_seq_order CHECK (destination_stop_seq > origin_stop_seq),
    INDEX idx_wl_queue (run_id, travel_class, position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. PAYMENTS TABLE
DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL DEFAULT 'SIMULATED_UPI',
    transaction_reference VARCHAR(60) NOT NULL UNIQUE,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',
    paid_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    CONSTRAINT chk_payment_amount_nonneg CHECK (amount >= 0),
    INDEX idx_pay_txn_ref (transaction_reference)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. CANCELLATIONS TABLE
DROP TABLE IF EXISTS cancellations;
CREATE TABLE cancellations (
    cancellation_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    cancellation_reason VARCHAR(255) NOT NULL,
    cancellation_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    refund_amount DECIMAL(10, 2) NOT NULL,
    refund_status VARCHAR(20) NOT NULL DEFAULT 'PROCESSED',
    cancelled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cancel_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE RESTRICT,
    CONSTRAINT chk_cancel_fee_nonneg CHECK (cancellation_fee >= 0),
    CONSTRAINT chk_refund_amt_nonneg CHECK (refund_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
