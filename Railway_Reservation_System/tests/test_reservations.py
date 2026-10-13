"""
Reservation and Booking Workflow Tests.
Verifies transaction safety, PNR generation, payment reconciliation, and waitlist routing.
"""
import pytest
from app.models.booking import Booking
from app.models.schedule import TrainRun
from app.models.passenger import Passenger
from app.models.station import Station
from app.services.booking_service import book_ticket


def test_valid_booking_success(db_session):
    """Test standard confirmed ticket booking workflow."""
    run = TrainRun.query.first()
    passenger = Passenger.query.first()
    stn_ndls = Station.query.filter_by(station_code='NDLS').first()
    stn_pryj = Station.query.filter_by(station_code='PRYJ').first()

    result = book_ticket(
        run_id=run.run_id,
        passenger_id=passenger.passenger_id,
        origin_station_id=stn_ndls.station_id,
        destination_station_id=stn_pryj.station_id,
        travel_class='CC'
    )

    assert result['status'] == 'CONFIRMED'
    assert 'pnr_number' in result
    assert result['fare'] > 0

    # Verify database state
    b = Booking.query.filter_by(pnr_number=result['pnr_number']).first()
    assert b is not None
    assert b.booking_status == 'CONFIRMED'
    assert b.payment is not None
    assert b.payment.payment_status == 'COMPLETED'
    assert len(b.journey_segments) == 1
    assert b.journey_segments[0].allocation_status == 'ACTIVE'


def test_invalid_origin_dest_sequence_fails(db_session):
    """Test that attempting to book backwards (dest before origin) is rejected."""
    run = TrainRun.query.first()
    passenger = Passenger.query.first()
    stn_ndls = Station.query.filter_by(station_code='NDLS').first()
    stn_bsb = Station.query.filter_by(station_code='BSB').first()

    # BSB is stop 4, NDLS is stop 1. Train travels 1 -> 4, not 4 -> 1.
    with pytest.raises(ValueError, match="Origin stop sequence must precede destination stop sequence"):
        book_ticket(
            run_id=run.run_id,
            passenger_id=passenger.passenger_id,
            origin_station_id=stn_bsb.station_id,
            destination_station_id=stn_ndls.station_id,
            travel_class='CC'
        )


def test_train_runs_isolation(db_session):
    """Test that reservations on different dates do not conflict with each other."""
    runs = TrainRun.query.filter_by(train_id=1).all()
    assert len(runs) >= 2
    run1 = runs[0]
    run2 = runs[1]
    passenger = Passenger.query.first()
    stn_ndls = Station.query.filter_by(station_code='NDLS').first()
    stn_bsb = Station.query.filter_by(station_code='BSB').first()

    # Book full route on run1
    res1 = book_ticket(
        run_id=run1.run_id,
        passenger_id=passenger.passenger_id,
        origin_station_id=stn_ndls.station_id,
        destination_station_id=stn_bsb.station_id,
        travel_class='1A'
    )
    # Book full route on run2
    res2 = book_ticket(
        run_id=run2.run_id,
        passenger_id=passenger.passenger_id,
        origin_station_id=stn_ndls.station_id,
        destination_station_id=stn_bsb.station_id,
        travel_class='1A'
    )

    assert res1['pnr_number'] != res2['pnr_number']
    assert res1['status'] in ('CONFIRMED', 'WAITLISTED')
    assert res2['status'] in ('CONFIRMED', 'WAITLISTED')
