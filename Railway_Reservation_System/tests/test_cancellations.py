"""
Cancellation, Refund Policy, and Automated Waitlist Promotion Tests.
"""
import pytest
from app.models.booking import Booking
from app.models.journey_segment import JourneySegment
from app.models.cancellation import Cancellation
from app.models.waitlist import Waitlist
from app.services.cancellation_service import cancel_booking


def test_eligible_cancellation_and_refund_policy(db_session):
    """Test standard ticket cancellation, fee deduction, and refund calculation."""
    # Booking 1 is confirmed in seed data
    b = Booking.query.filter_by(booking_status='CONFIRMED').first()
    orig_fare = float(b.total_fare)

    res = cancel_booking(b.booking_id, reason="Testing cancellation policy")

    assert res['cancellation_id'] is not None
    assert res['cancellation_fee'] == pytest.approx(orig_fare * 0.20, 0.01)
    assert res['refund_amount'] == pytest.approx(orig_fare * 0.80, 0.01)

    # Verify database updates
    assert b.booking_status == 'CANCELLED'
    for seg in b.journey_segments:
        assert seg.allocation_status == 'CANCELLED'

    canc = Cancellation.query.filter_by(booking_id=b.booking_id).first()
    assert canc is not None
    assert canc.refund_status == 'PROCESSED'


def test_duplicate_cancellation_rejected(db_session):
    """Verify that attempting to cancel an already cancelled booking raises ValueError."""
    # Booking 4 is already cancelled in seed data
    b_cancelled = Booking.query.filter_by(booking_status='CANCELLED').first()

    with pytest.raises(ValueError, match="already been cancelled"):
        cancel_booking(b_cancelled.booking_id)


def test_automated_waitlist_promotion(db_session):
    """
    Test that cancelling a confirmed ticket automatically promotes the next eligible waitlist candidate.
    """
    # Find a waitlisted booking in seed data
    wl_entry = Waitlist.query.filter_by(waitlist_status='WAITING').first()
    assert wl_entry is not None
    target_run_id = wl_entry.run_id
    target_class = wl_entry.travel_class
    promoted_pnr_expected = wl_entry.booking.pnr_number

    # Find a confirmed booking on that same run and class that overlaps with candidate
    conf_booking = (
        Booking.query
        .filter_by(run_id=target_run_id, travel_class=target_class, booking_status='CONFIRMED')
        .first()
    )

    if conf_booking:
        res = cancel_booking(conf_booking.booking_id)
        # Check if candidate was promoted
        assert res['promoted_pnr'] == promoted_pnr_expected
        assert wl_entry.waitlist_status == 'PROMOTED'
        assert wl_entry.booking.booking_status == 'CONFIRMED'
        # Check active journey segment was assigned to promoted passenger
        active_seg = JourneySegment.query.filter_by(booking_id=wl_entry.booking_id, allocation_status='ACTIVE').first()
        assert active_seg is not None
