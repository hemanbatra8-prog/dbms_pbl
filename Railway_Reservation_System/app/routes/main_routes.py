"""
Main application routes.
Dashboard and overview.
"""
from flask import Blueprint, render_template
from app.services.report_service import get_dashboard_metrics
from app.models.booking import Booking

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    metrics = get_dashboard_metrics()
    recent_bookings = Booking.query.order_by(Booking.booked_at.desc()).limit(8).all()
    return render_template('dashboard.html', metrics=metrics, recent_bookings=recent_bookings)
