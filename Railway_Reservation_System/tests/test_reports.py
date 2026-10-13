"""
SQL Reports and Analytics Verification Tests.
Verifies that all 12 benchmark SQL reporting queries execute cleanly against the database schema.
"""
from app.services import report_service


def test_all_12_reports_execute_successfully(db_session):
    """Executes all 12 benchmark reports and confirms valid record output."""
    r1 = report_service.report_1_segment_availability()
    assert isinstance(r1, list)
    assert len(r1) > 0

    r2 = report_service.report_2_passenger_booking_history()
    assert isinstance(r2, list)
    assert len(r2) > 0

    r3 = report_service.report_3_waitlist_queue_summary()
    assert isinstance(r3, list)

    r4 = report_service.report_4_coach_occupancy_percentage()
    assert isinstance(r4, list)
    assert len(r4) > 0

    r5 = report_service.report_5_route_demand_analysis()
    assert isinstance(r5, list)
    assert len(r5) > 0

    r6 = report_service.report_6_cancellation_and_refunds()
    assert isinstance(r6, list)
    assert len(r6) > 0

    r7 = report_service.report_7_passenger_journey_details()
    assert isinstance(r7, list)
    assert len(r7) > 0

    r8 = report_service.report_8_revenue_by_train_and_class()
    assert isinstance(r8, list)

    r9 = report_service.report_9_financial_reconciliation()
    assert isinstance(r9, list)
    assert len(r9) == 5

    r10 = report_service.report_10_booking_status_distribution()
    assert isinstance(r10, list)
    assert len(r10) > 0

    r11 = report_service.report_11_train_stop_timetable()
    assert isinstance(r11, list)
    assert len(r11) > 0

    r12 = report_service.report_12_top_passengers_by_revenue()
    assert isinstance(r12, list)
    assert len(r12) > 0
