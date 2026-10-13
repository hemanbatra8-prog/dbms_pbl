"""
Segment-Wise Seat Availability Tests.
Verifies the half-open interval overlap algorithm: [s, e) overlaps [r_start, r_end) iff s < r_end AND r_start < e.
"""
from app.models.journey_segment import JourneySegment
from app.models.schedule import TrainRun
from app.services.availability_service import get_available_seats, get_occupied_seat_ids


def test_interval_overlap_logic():
    """Unit test the pure interval overlap mathematical condition."""
    seg = JourneySegment(start_stop_seq=2, end_stop_seq=4, allocation_status='ACTIVE')

    # [1, 2) does NOT overlap [2, 4): 1 < 4 (True) but 2 < 2 (False) -> False
    assert seg.overlaps_with(1, 2) is False

    # [4, 5) does NOT overlap [2, 4): 2 < 5 (True) but 4 < 4 (False) -> False
    assert seg.overlaps_with(4, 5) is False

    # [1, 3) DOES overlap [2, 4): 2 < 3 (True) and 1 < 4 (True) -> True
    assert seg.overlaps_with(1, 3) is True

    # [3, 4) DOES overlap [2, 4): 2 < 4 (True) and 3 < 4 (True) -> True
    assert seg.overlaps_with(3, 4) is True

    # Cancelled segment must NOT overlap
    seg.allocation_status = 'CANCELLED'
    assert seg.overlaps_with(1, 3) is False


def test_non_overlapping_seat_reuse(db_session):
    """
    Test that the same seat can be allocated for adjacent non-overlapping segments on the same train run.
    In seed data:
    - Passenger 1 has Seat C1-1 on segment [1, 2) (NDLS -> CNB)
    - Passenger 2 has Seat C1-1 on segment [2, 4) (CNB -> BSB)
    Both are ACTIVE.
    """
    run = TrainRun.query.first()
    # Check occupied seats for [1, 2)
    occupied_1_2 = get_occupied_seat_ids(run.run_id, 1, 2)
    # Check occupied seats for [2, 4)
    occupied_2_4 = get_occupied_seat_ids(run.run_id, 2, 4)

    # Seat C1-1 is in both occupied sets
    c1_1_id = 1
    assert c1_1_id in occupied_1_2
    assert c1_1_id in occupied_2_4


def test_conflicting_interval_detection(db_session):
    """
    Test that a request for [1, 4) (NDLS -> BSB) identifies Seat C1-1 as occupied because
    [1, 4) overlaps with [1, 2) and [2, 4).
    """
    run = TrainRun.query.first()
    occupied_1_4 = get_occupied_seat_ids(run.run_id, 1, 4)
    c1_1_id = 1
    assert c1_1_id in occupied_1_4


def test_cancelled_allocation_restores_availability(db_session):
    """
    Test that when an allocation status is CANCELLED, that seat becomes available again for overlapping segments.
    """
    run = TrainRun.query.first()
    # In seed data, Seat C1-3 was cancelled for segment [1, 2)
    c1_3_id = 3
    occupied_1_2 = get_occupied_seat_ids(run.run_id, 1, 2)
    assert c1_3_id not in occupied_1_2  # Seat C1-3 is FREE because allocation was cancelled!
