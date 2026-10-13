"""
Booking Service.
Implements transaction-safe reservation and seat allocation workflows.
Uses row locking and atomic database transactions to eliminate race conditions.
"""
import uuid
import random
from decimal import Decimal
from app.extensions import db
from app.models.schedule import TrainRun
from app.models.passenger import Passenger
from app.models.station import Station
from app.models.route import TrainStop
from app.models.coach import Seat
from app.models.booking import Booking
from app.models.journey_segment import JourneySegment
from app.models.waitlist import Waitlist
from app.models.payment import Payment
from app.services.availability_service import get_available_seats
from app.services.fare_service import calculate_journey_fare


def generate_pnr() -> str:
    """Generates a realistic 10-digit PNR string."""
    prefix = random.randint(100, 999)
    suffix = random.randint(1000000, 9999999)
    return f"{prefix}{suffix}"


def generate_txn_ref() -> str:
    """Generates a unique payment transaction reference."""
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


def book_ticket(
    run_id: int,
    passenger_id: int,
    origin_station_id: int,
    destination_station_id: int,
    travel_class: str,
    preferred_seat_id: int = None,
    payment_method: str = 'SIMULATED_UPI'
) -> dict:
    """
    Executes a transaction-safe railway reservation.
    Ensures that seat availability checking and journey segment insertion happen atomically.
    """
    # 1. Basic entity validations
    run = db.session.get(TrainRun, run_id)
    if not run or run.status != 'SCHEDULED':
        raise ValueError("Selected train run is not currently available for reservation.")

    passenger = db.session.get(Passenger, passenger_id)
    if not passenger:
        raise ValueError("Passenger record not found.")

    origin_stn = db.session.get(Station, origin_station_id)
    dest_stn = db.session.get(Station, destination_station_id)
    if not origin_stn or not dest_stn:
        raise ValueError("Invalid origin or destination station.")

    route = run.train.route
    origin_stop = TrainStop.query.filter_by(route_id=route.route_id, station_id=origin_station_id).first()
    dest_stop = TrainStop.query.filter_by(route_id=route.route_id, station_id=destination_station_id).first()

    if not origin_stop or not dest_stop:
        raise ValueError("Selected stations do not lie on this train's scheduled route.")

    if origin_stop.stop_sequence >= dest_stop.stop_sequence:
        raise ValueError("Origin stop sequence must precede destination stop sequence.")

    origin_seq = origin_stop.stop_sequence
    dest_seq = dest_stop.stop_sequence

    # 2. Fare calculation
    total_fare = calculate_journey_fare(run.train.train_type, travel_class, origin_stop, dest_stop)

    # 3. Transaction-safe allocation
    try:
        # Lock the TrainRun row to serialize concurrent reservations for this train run
        # In MySQL/Postgres, with_for_update() enforces row-level exclusive lock
        locked_run = TrainRun.query.filter_by(run_id=run_id).with_for_update().first()

        # Query available seats under the lock
        available_seats = get_available_seats(run_id, travel_class, origin_seq, dest_seq)

        pnr = generate_pnr()
        while Booking.query.filter_by(pnr_number=pnr).first():
            pnr = generate_pnr()

        if len(available_seats) > 0:
            # Choose preferred seat if valid and free, otherwise pick first available
            chosen_seat = None
            if preferred_seat_id:
                for s in available_seats:
                    if s.seat_id == preferred_seat_id:
                        chosen_seat = s
                        break
            if not chosen_seat:
                chosen_seat = available_seats[0]

            # Create Confirmed Booking
            booking = Booking(
                pnr_number=pnr,
                run_id=run_id,
                passenger_id=passenger_id,
                origin_station_id=origin_station_id,
                destination_station_id=destination_station_id,
                origin_stop_seq=origin_seq,
                destination_stop_seq=dest_seq,
                travel_class=travel_class,
                booking_status='CONFIRMED',
                total_fare=total_fare
            )
            db.session.add(booking)
            db.session.flush()  # Populates booking_id

            # Create Journey Segment record for the half-open interval [origin_seq, dest_seq)
            segment = JourneySegment(
                booking_id=booking.booking_id,
                seat_id=chosen_seat.seat_id,
                run_id=run_id,
                start_stop_seq=origin_seq,
                end_stop_seq=dest_seq,
                allocation_status='ACTIVE'
            )
            db.session.add(segment)

            # Create Payment record
            payment = Payment(
                booking_id=booking.booking_id,
                amount=total_fare,
                payment_method=payment_method,
                transaction_reference=generate_txn_ref(),
                payment_status='COMPLETED'
            )
            db.session.add(payment)

            db.session.commit()
            return {
                'status': 'CONFIRMED',
                'booking_id': booking.booking_id,
                'pnr_number': booking.pnr_number,
                'seat_label': f"{chosen_seat.coach.coach_code}-{chosen_seat.seat_number}",
                'berth_type': chosen_seat.berth_type,
                'fare': float(total_fare),
                'message': f"Booking confirmed on Seat {chosen_seat.coach.coach_code}-{chosen_seat.seat_number} ({chosen_seat.berth_type})"
            }

        else:
            # No seat available -> Allocate to waitlist
            active_wl_max = (
                db.session.query(db.func.max(Waitlist.position))
                .filter_by(run_id=run_id, travel_class=travel_class, waitlist_status='WAITING')
                .scalar()
            )
            next_position = (active_wl_max or 0) + 1

            booking = Booking(
                pnr_number=pnr,
                run_id=run_id,
                passenger_id=passenger_id,
                origin_station_id=origin_station_id,
                destination_station_id=destination_station_id,
                origin_stop_seq=origin_seq,
                destination_stop_seq=dest_seq,
                travel_class=travel_class,
                booking_status='WAITLISTED',
                total_fare=total_fare
            )
            db.session.add(booking)
            db.session.flush()

            waitlist_entry = Waitlist(
                booking_id=booking.booking_id,
                run_id=run_id,
                travel_class=travel_class,
                origin_stop_seq=origin_seq,
                destination_stop_seq=dest_seq,
                position=next_position,
                waitlist_status='WAITING'
            )
            db.session.add(waitlist_entry)

            payment = Payment(
                booking_id=booking.booking_id,
                amount=total_fare,
                payment_method=payment_method,
                transaction_reference=generate_txn_ref(),
                payment_status='COMPLETED'
            )
            db.session.add(payment)

            db.session.commit()
            return {
                'status': 'WAITLISTED',
                'booking_id': booking.booking_id,
                'pnr_number': booking.pnr_number,
                'waitlist_position': next_position,
                'fare': float(total_fare),
                'message': f"No seats currently available. Booking placed on Waitlist at Position WL#{next_position}."
            }

    except Exception as e:
        db.session.rollback()
        raise e
