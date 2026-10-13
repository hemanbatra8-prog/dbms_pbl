"""
Report Service.
Executes advanced SQL queries demonstrating joins, aggregations, nested queries, and financial reconciliation.
Powers the 12 required DBMS reports.
"""
from sqlalchemy import func, distinct, case
from app.extensions import db
from app.models.station import Station
from app.models.route import Route, TrainStop
from app.models.train import Train
from app.models.schedule import TrainRun
from app.models.coach import Coach, Seat
from app.models.passenger import Passenger
from app.models.booking import Booking
from app.models.journey_segment import JourneySegment
from app.models.waitlist import Waitlist
from app.models.payment import Payment
from app.models.cancellation import Cancellation


def get_dashboard_metrics():
    """Returns top-level operational and financial KPIs."""
    total_trains = Train.query.count()
    total_passengers = Passenger.query.count()
    total_bookings = Booking.query.count()
    confirmed_bookings = Booking.query.filter_by(booking_status='CONFIRMED').count()
    waitlisted_bookings = Booking.query.filter_by(booking_status='WAITLISTED').count()
    cancelled_bookings = Booking.query.filter_by(booking_status='CANCELLED').count()

    # Net revenue = Total Payments Collected - Total Refunds
    total_payments = db.session.query(func.coalesce(func.sum(Payment.amount), 0)).scalar()
    total_refunds = db.session.query(func.coalesce(func.sum(Cancellation.refund_amount), 0)).scalar()
    net_revenue = float(total_payments) - float(total_refunds)

    return {
        'total_trains': total_trains,
        'total_passengers': total_passengers,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'waitlisted_bookings': waitlisted_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_payments': float(total_payments),
        'total_refunds': float(total_refunds),
        'net_revenue': round(net_revenue, 2)
    }


def report_1_segment_availability():
    """Report 1: Segment-wise availability summary by train run and travel class."""
    # Aggregation of total seats per train/class vs active allocated segments
    sql = """
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
    """
    result = db.session.execute(db.text(sql)).fetchall()
    return [dict(r._mapping) for r in result]


def report_2_passenger_booking_history(passenger_id=None):
    """Report 2: Passenger booking history with train, date, and status."""
    query = (
        db.session.query(
            Booking.pnr_number,
            Passenger.full_name,
            Train.train_number,
            Train.train_name,
            TrainRun.run_date,
            Booking.travel_class,
            Booking.booking_status,
            Booking.total_fare,
            Booking.booked_at
        )
        .join(Passenger, Booking.passenger_id == Passenger.passenger_id)
        .join(TrainRun, Booking.run_id == TrainRun.run_id)
        .join(Train, TrainRun.train_id == Train.train_id)
    )
    if passenger_id:
        query = query.filter(Booking.passenger_id == passenger_id)
    query = query.order_by(Booking.booked_at.desc())

    records = query.all()
    return [{
        'pnr_number': r[0],
        'full_name': r[1],
        'train_number': r[2],
        'train_name': r[3],
        'run_date': r[4].strftime('%Y-%m-%d'),
        'travel_class': r[5],
        'booking_status': r[6],
        'total_fare': float(r[7]),
        'booked_at': r[8].strftime('%Y-%m-%d %H:%M')
    } for r in records]


def report_3_waitlist_queue_summary():
    """Report 3: Active Waitlist positions and passenger details."""
    records = (
        db.session.query(
            Waitlist.waitlist_id,
            Waitlist.position,
            Waitlist.waitlist_status,
            Booking.pnr_number,
            Passenger.full_name,
            Train.train_number,
            Train.train_name,
            TrainRun.run_date,
            Waitlist.travel_class,
            Waitlist.created_at
        )
        .join(Booking, Waitlist.booking_id == Booking.booking_id)
        .join(Passenger, Booking.passenger_id == Passenger.passenger_id)
        .join(TrainRun, Waitlist.run_id == TrainRun.run_id)
        .join(Train, TrainRun.train_id == Train.train_id)
        .order_by(TrainRun.run_date, Waitlist.travel_class, Waitlist.position)
        .all()
    )
    return [{
        'waitlist_id': r[0],
        'position': r[1],
        'status': r[2],
        'pnr_number': r[3],
        'passenger_name': r[4],
        'train_number': r[5],
        'train_name': r[6],
        'run_date': r[7].strftime('%Y-%m-%d'),
        'travel_class': r[8],
        'created_at': r[9].strftime('%Y-%m-%d %H:%M')
    } for r in records]


def report_4_coach_occupancy_percentage():
    """Report 4: Coach occupancy rate calculation using nested aggregation."""
    sql = """
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
    """
    result = db.session.execute(db.text(sql)).fetchall()
    return [dict(r._mapping) for r in result]


def report_5_route_demand_analysis():
    """Report 5: Route popularity by booking volume and passenger count."""
    sql = """
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
    """
    result = db.session.execute(db.text(sql)).fetchall()
    return [dict(r._mapping) for r in result]


def report_6_cancellation_and_refunds():
    """Report 6: Summary of ticket cancellations, fee deductions, and refunds."""
    records = (
        db.session.query(
            Cancellation.cancellation_id,
            Booking.pnr_number,
            Passenger.full_name,
            Cancellation.cancellation_reason,
            Cancellation.cancellation_fee,
            Cancellation.refund_amount,
            Cancellation.refund_status,
            Cancellation.cancelled_at
        )
        .join(Booking, Cancellation.booking_id == Booking.booking_id)
        .join(Passenger, Booking.passenger_id == Passenger.passenger_id)
        .order_by(Cancellation.cancelled_at.desc())
        .all()
    )
    return [{
        'cancellation_id': r[0],
        'pnr_number': r[1],
        'passenger_name': r[2],
        'reason': r[3],
        'cancellation_fee': float(r[4]),
        'refund_amount': float(r[5]),
        'refund_status': r[6],
        'cancelled_at': r[7].strftime('%Y-%m-%d %H:%M')
    } for r in records]


def report_7_passenger_journey_details():
    """Report 7: Detailed journey itinerary for passengers with station timings."""
    sql = """
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
    """
    result = db.session.execute(db.text(sql)).fetchall()
    return [dict(r._mapping) for r in result]


def report_8_revenue_by_train_and_class():
    """Report 8: Revenue collected grouped by train and travel class."""
    sql = """
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
    """
    result = db.session.execute(db.text(sql)).fetchall()
    return [dict(r._mapping) for r in result]


def report_9_financial_reconciliation():
    """Report 9: Financial audit reconciling bookings, payments, and refunds."""
    total_booking_fare = db.session.query(func.coalesce(func.sum(Booking.total_fare), 0)).scalar()
    total_paid = db.session.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.payment_status.in_(['COMPLETED', 'REFUNDED'])).scalar()
    total_refunded = db.session.query(func.coalesce(func.sum(Cancellation.refund_amount), 0)).scalar()
    total_cancellation_fees = db.session.query(func.coalesce(func.sum(Cancellation.cancellation_fee), 0)).scalar()
    net_revenue = float(total_paid) - float(total_refunded)

    return [{
        'metric': 'Total Booking Value (Gross)',
        'amount': float(total_booking_fare)
    }, {
        'metric': 'Total Payments Processed',
        'amount': float(total_paid)
    }, {
        'metric': 'Total Refunds Disbursed to Passengers',
        'amount': float(total_refunded)
    }, {
        'metric': 'Total Cancellation Fees Retained',
        'amount': float(total_cancellation_fees)
    }, {
        'metric': 'Net Retained Revenue',
        'amount': round(net_revenue, 2)
    }]


def report_10_booking_status_distribution():
    """Report 10: Status distribution (Confirmed vs Waitlisted vs Cancelled)."""
    sql = """
    SELECT 
        booking_status,
        COUNT(*) AS booking_count,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bookings)), 2) AS percentage
    FROM bookings
    GROUP BY booking_status;
    """
    result = db.session.execute(db.text(sql)).fetchall()
    return [dict(r._mapping) for r in result]


def report_11_train_stop_timetable(train_id=None):
    """Report 11: Route stops, sequences, distance, and timetable."""
    query = (
        db.session.query(
            Train.train_number,
            Train.train_name,
            Route.route_code,
            TrainStop.stop_sequence,
            Station.station_code,
            Station.station_name,
            TrainStop.distance_from_source_km,
            TrainStop.arrival_time,
            TrainStop.departure_time
        )
        .join(Route, Train.route_id == Route.route_id)
        .join(TrainStop, Route.route_id == TrainStop.route_id)
        .join(Station, TrainStop.station_id == Station.station_id)
    )
    if train_id:
        query = query.filter(Train.train_id == train_id)
    query = query.order_by(Train.train_number, TrainStop.stop_sequence)

    records = query.all()
    return [{
        'train_number': r[0],
        'train_name': r[1],
        'route_code': r[2],
        'stop_sequence': r[3],
        'station_code': r[4],
        'station_name': r[5],
        'distance_km': float(r[6]),
        'arrival_time': r[7].strftime('%H:%M') if r[7] else '--',
        'departure_time': r[8].strftime('%H:%M') if r[8] else '--'
    } for r in records]


def report_12_top_passengers_by_revenue():
    """Report 12: Frequent passengers ranked by total expenditure and booking count (Nested Query)."""
    sql = """
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
    """
    result = db.session.execute(db.text(sql)).fetchall()
    return [dict(r._mapping) for r in result]
