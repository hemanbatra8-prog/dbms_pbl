"""
Booking Routes.
Handles ticket reservation workflows, PNR generation, and status inquiries.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.schedule import TrainRun
from app.models.station import Station
from app.models.passenger import Passenger
from app.models.booking import Booking
from app.models.route import TrainStop
from app.services.booking_service import book_ticket
from app.services.fare_service import calculate_journey_fare
from app.services.availability_service import get_available_seats

booking_bp = Blueprint('bookings', __name__)


@booking_bp.route('/book', methods=['GET', 'POST'])
def book():
    run_id = request.args.get('run_id', type=int)
    travel_class = request.args.get('travel_class', type=str, default='3A')
    origin_id = request.args.get('origin_id', type=int)
    dest_id = request.args.get('dest_id', type=int)

    if request.method == 'POST':
        try:
            run_id = int(request.form.get('run_id'))
            passenger_id = int(request.form.get('passenger_id'))
            origin_id = int(request.form.get('origin_id'))
            dest_id = int(request.form.get('dest_id'))
            travel_class = request.form.get('travel_class')
            preferred_seat_id = request.form.get('preferred_seat_id')
            preferred_seat_id = int(preferred_seat_id) if preferred_seat_id else None
            payment_method = request.form.get('payment_method', 'SIMULATED_UPI')

            result = book_ticket(
                run_id=run_id,
                passenger_id=passenger_id,
                origin_station_id=origin_id,
                destination_station_id=dest_id,
                travel_class=travel_class,
                preferred_seat_id=preferred_seat_id,
                payment_method=payment_method
            )

            flash(result['message'], "success" if result['status'] == 'CONFIRMED' else "warning")
            return redirect(url_for('bookings.booking_detail', pnr=result['pnr_number']))

        except Exception as e:
            flash(f"Booking failed: {str(e)}", "danger")

    # Load context data for booking form
    run = db.session.get(TrainRun, run_id) if run_id else None
    passengers = Passenger.query.order_by(Passenger.full_name).all()
    stations = Station.query.order_by(Station.station_code).all()

    origin_stn = db.session.get(Station, origin_id) if origin_id else None
    dest_stn = db.session.get(Station, dest_id) if dest_id else None

    fare_amount = None
    available_seats = []
    if run and origin_stn and dest_stn:
        origin_stop = TrainStop.query.filter_by(route_id=run.train.route_id, station_id=origin_id).first()
        dest_stop = TrainStop.query.filter_by(route_id=run.train.route_id, station_id=dest_id).first()
        if origin_stop and dest_stop and origin_stop.stop_sequence < dest_stop.stop_sequence:
            fare_amount = calculate_journey_fare(run.train.train_type, travel_class, origin_stop, dest_stop)
            available_seats = get_available_seats(run_id, travel_class, origin_stop.stop_sequence, dest_stop.stop_sequence)

    return render_template(
        'book.html',
        run=run,
        passengers=passengers,
        stations=stations,
        origin_stn=origin_stn,
        dest_stn=dest_stn,
        travel_class=travel_class,
        fare_amount=float(fare_amount) if fare_amount else None,
        available_seats=available_seats
    )


@booking_bp.route('/booking/<pnr>')
def booking_detail(pnr):
    booking = Booking.query.filter_by(pnr_number=pnr).first_or_404()
    return render_template('booking_detail.html', booking=booking)


@booking_bp.route('/pnr', methods=['GET', 'POST'])
def pnr_inquiry():
    pnr_query = request.args.get('pnr', '').strip()
    booking = None
    error = None

    if pnr_query:
        booking = Booking.query.filter_by(pnr_number=pnr_query).first()
        if not booking:
            error = f"PNR '{pnr_query}' not found. Please verify the 10-digit number."

    return render_template('pnr_inquiry.html', booking=booking, pnr_query=pnr_query, error=error)
