"""
Administration and Database Inspection Routes.
Provides table row counts, schema status, and seed control.
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db
from app.models import (
    Station, Route, Train, TrainStop, TrainRun, Coach, Seat,
    Passenger, FareRule, Booking, JourneySegment, Waitlist,
    Payment, Cancellation
)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def admin_panel():
    table_stats = [
        {'name': 'Stations', 'count': Station.query.count()},
        {'name': 'Routes', 'count': Route.query.count()},
        {'name': 'Trains', 'count': Train.query.count()},
        {'name': 'Train Stops', 'count': TrainStop.query.count()},
        {'name': 'Train Runs (Schedules)', 'count': TrainRun.query.count()},
        {'name': 'Coaches', 'count': Coach.query.count()},
        {'name': 'Seats', 'count': Seat.query.count()},
        {'name': 'Passengers', 'count': Passenger.query.count()},
        {'name': 'Fare Rules', 'count': FareRule.query.count()},
        {'name': 'Bookings', 'count': Booking.query.count()},
        {'name': 'Journey Segments', 'count': JourneySegment.query.count()},
        {'name': 'Waitlist Entries', 'count': Waitlist.query.count()},
        {'name': 'Payments', 'count': Payment.query.count()},
        {'name': 'Cancellations', 'count': Cancellation.query.count()},
    ]

    engine_name = db.engine.name
    return render_template('admin.html', table_stats=table_stats, engine_name=engine_name)


@admin_bp.route('/admin/reseed', methods=['POST'])
def reseed_database():
    from database.seed_data import populate_seed_data
    try:
        populate_seed_data(db.session)
        flash("Database successfully reset and seeded with realistic railway sample dataset!", "success")
    except Exception as e:
        flash(f"Error resetting database: {str(e)}", "danger")
    return redirect(url_for('admin.admin_panel'))
