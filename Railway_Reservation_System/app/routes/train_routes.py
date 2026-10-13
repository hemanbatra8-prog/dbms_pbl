"""
Train and Search Routes.
Handles train discovery, timetable inspection, and live seat availability checks.
"""
from datetime import datetime, date
from flask import Blueprint, render_template, request, jsonify
from app.models.station import Station
from app.models.train import Train
from app.models.route import TrainStop
from app.models.schedule import TrainRun
from app.services.availability_service import find_trains_between_stations, get_available_seats

train_bp = Blueprint('trains', __name__)


@train_bp.route('/search', methods=['GET', 'POST'])
def search_trains():
    stations = Station.query.order_by(Station.station_code).all()
    results = None
    origin_code = request.args.get('origin', '')
    dest_code = request.args.get('destination', '')
    travel_date_str = request.args.get('date', '')

    if origin_code and dest_code and travel_date_str:
        try:
            travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
            results = find_trains_between_stations(origin_code, dest_code, travel_date)
        except ValueError:
            results = []

    return render_template(
        'search.html',
        stations=stations,
        results=results,
        origin_code=origin_code,
        dest_code=dest_code,
        travel_date_str=travel_date_str
    )


@train_bp.route('/trains')
def train_list():
    trains = Train.query.order_by(Train.train_number).all()
    return render_template('train_list.html', trains=trains)


@train_bp.route('/api/available-seats')
def api_available_seats():
    run_id = request.args.get('run_id', type=int)
    travel_class = request.args.get('travel_class', type=str)
    origin_id = request.args.get('origin_id', type=int)
    dest_id = request.args.get('dest_id', type=int)

    if not all([run_id, travel_class, origin_id, dest_id]):
        return jsonify({'error': 'Missing parameters'}), 400

    from app.extensions import db
    run = db.session.get(TrainRun, run_id)
    if not run:
        return jsonify({'error': 'Train run not found'}), 404

    origin_stop = TrainStop.query.filter_by(route_id=run.train.route_id, station_id=origin_id).first()
    dest_stop = TrainStop.query.filter_by(route_id=run.train.route_id, station_id=dest_id).first()

    if not origin_stop or not dest_stop or origin_stop.stop_sequence >= dest_stop.stop_sequence:
        return jsonify({'error': 'Invalid stop sequence'}), 400

    seats = get_available_seats(run_id, travel_class, origin_stop.stop_sequence, dest_stop.stop_sequence)
    return jsonify({
        'available_count': len(seats),
        'seats': [{
            'seat_id': s.seat_id,
            'coach_code': s.coach.coach_code,
            'seat_number': s.seat_number,
            'berth_type': s.berth_type
        } for s in seats]
    })
