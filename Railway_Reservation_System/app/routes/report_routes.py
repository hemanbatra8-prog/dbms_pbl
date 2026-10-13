"""
Report and Analytics Routes.
Renders all 12 advanced SQL reports for academic reviews and audits.
"""
from flask import Blueprint, render_template, request
from app.services import report_service

report_bp = Blueprint('reports', __name__)

REPORT_DEFINITIONS = {
    '1': ('Report 1: Segment-Wise Seat Availability Summary', report_service.report_1_segment_availability, 'availability'),
    '2': ('Report 2: Passenger Booking History', report_service.report_2_passenger_booking_history, 'history'),
    '3': ('Report 3: Active Waitlist Queue Summary', report_service.report_3_waitlist_queue_summary, 'waitlist'),
    '4': ('Report 4: Coach Occupancy Percentage', report_service.report_4_coach_occupancy_percentage, 'occupancy'),
    '5': ('Report 5: Route Demand & Volume Analysis', report_service.report_5_route_demand_analysis, 'routes'),
    '6': ('Report 6: Ticket Cancellations & Refunds Audit', report_service.report_6_cancellation_and_refunds, 'cancellations'),
    '7': ('Report 7: Passenger Complete Journey Itinerary', report_service.report_7_passenger_journey_details, 'itinerary'),
    '8': ('Report 8: Revenue by Train and Travel Class', report_service.report_8_revenue_by_train_and_class, 'revenue'),
    '9': ('Report 9: Financial Reconciliation Audit', report_service.report_9_financial_reconciliation, 'reconciliation'),
    '10': ('Report 10: Booking Status Distribution (Confirmed vs WL vs Cancelled)', report_service.report_10_booking_status_distribution, 'distribution'),
    '11': ('Report 11: Route Timetable & Stop Distances', report_service.report_11_train_stop_timetable, 'timetable'),
    '12': ('Report 12: Frequent Passengers Ranked by Total Expenditure', report_service.report_12_top_passengers_by_revenue, 'frequent')
}


@report_bp.route('/reports')
def view_reports():
    active_report_id = request.args.get('id', '1')
    if active_report_id not in REPORT_DEFINITIONS:
        active_report_id = '1'

    report_title, report_func, template_type = REPORT_DEFINITIONS[active_report_id]
    data = report_func()

    return render_template(
        'reports.html',
        active_id=active_report_id,
        title=report_title,
        template_type=template_type,
        data=data,
        report_defs=REPORT_DEFINITIONS
    )
