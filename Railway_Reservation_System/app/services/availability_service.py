"""
Availability Service.
Implements the crucial segment-wise seat availability algorithm.
Calculates availability for half-open intervals [origin_stop_seq, dest_stop_seq) using relational queries.
"""
from datetime import date
from sqlalchemy import and_
from app.extensions import db
from app.models.station import Station
from app.models.route import Route, TrainStop
from app.models.train import Train
from app.models.schedule import TrainRun
from app.models.coach import Coach, Seat
from app.models.journey_segment import JourneySegment
from app.models.waitlist import Waitlist
from app.services.fare_service import calculate_journey_fare


def find_trains_between_stations(origin_code: str, dest_code: str, travel_date: date):
    """
    Finds trains running on travel_date that stop at origin_code before dest_code.
    Returns list of matching trains with route details and segment availability.
    """
    origin_stn = Station.query.filter_by(station_code=origin_code.upper()).first()
    dest_stn = Station.query.filter_by(station_code=dest_code.upper()).first()

    if not origin_stn or not dest_stn or origin_stn.station_id == dest_stn.station_id:
        return []

    # Query train runs on travel_date
    runs = (
        TrainRun.query
        .join(Train, TrainRun.train_id == Train.train_id)
        .filter(TrainRun.run_date == travel_date, TrainRun.status == 'SCHEDULED')
        .all()
    )

    results = []
    for run in runs:
        route = run.train.route
        origin_stop = TrainStop.query.filter_by(route_id=route.route_id, station_id=origin_stn.station_id).first()
        dest_stop = TrainStop.query.filter_by(route_id=route.route_id, station_id=dest_stn.station_id).first()

        # Both stations must be on route AND origin must be before destination
        if origin_stop and dest_stop and origin_stop.stop_sequence < dest_stop.stop_sequence:
            # Calculate availability for each travel class on this train
            classes = get_train_classes(run.train_id)
            class_availabilities = {}
            for t_class in classes:
                avail_seats = get_available_seats(run.run_id, t_class, origin_stop.stop_sequence, dest_stop.stop_sequence)
                fare = calculate_journey_fare(run.train.train_type, t_class, origin_stop, dest_stop)
                
                # Check waitlist count if no seats available
                wl_count = 0
                if len(avail_seats) == 0:
                    wl_count = Waitlist.query.filter_by(
                        run_id=run.run_id,
                        travel_class=t_class,
                        waitlist_status='WAITING'
                    ).count()

                class_availabilities[t_class] = {
                    'available_count': len(avail_seats),
                    'waitlist_count': wl_count,
                    'fare': float(fare),
                    'status_label': f"AVAILABLE {len(avail_seats)}" if len(avail_seats) > 0 else f"WL {wl_count + 1}"
                }

            distance = float(dest_stop.distance_from_source_km - origin_stop.distance_from_source_km)
            results.append({
                'run_id': run.run_id,
                'train_id': run.train.train_id,
                'train_number': run.train.train_number,
                'train_name': run.train.train_name,
                'train_type': run.train.train_type,
                'origin_stop': origin_stop,
                'dest_stop': dest_stop,
                'distance_km': distance,
                'departure_time': origin_stop.departure_time.strftime('%H:%M') if origin_stop.departure_time else '--',
                'arrival_time': dest_stop.arrival_time.strftime('%H:%M') if dest_stop.arrival_time else '--',
                'class_availabilities': class_availabilities
            })

    return results


def get_train_classes(train_id: int) -> list[str]:
    """Returns distinct travel classes available on a train."""
    classes = db.session.query(Coach.travel_class).filter(Coach.train_id == train_id).distinct().all()
    return [c[0] for c in classes]


def get_occupied_seat_ids(run_id: int, origin_seq: int, dest_seq: int) -> set[int]:
    """
    Finds all seat IDs that have an ACTIVE JourneySegment overlapping [origin_seq, dest_seq).
    Interval Overlap Formula:
    existing.start_stop_seq < dest_seq AND origin_seq < existing.end_stop_seq
    """
    overlapping_segments = (
        JourneySegment.query
        .filter(
            JourneySegment.run_id == run_id,
            JourneySegment.allocation_status == 'ACTIVE',
            JourneySegment.start_stop_seq < dest_seq,
            origin_seq < JourneySegment.end_stop_seq
        )
        .with_entities(JourneySegment.seat_id)
        .all()
    )
    return {seg.seat_id for seg in overlapping_segments}


def get_available_seats(run_id: int, travel_class: str, origin_seq: int, dest_seq: int) -> list[Seat]:
    """
    Returns list of free Seat objects for the given train run, class, and journey segment.
    """
    run = db.session.get(TrainRun, run_id)
    if not run:
        return []

    # All seats belonging to coaches of requested class on this train
    class_seats = (
        Seat.query
        .join(Coach, Seat.coach_id == Coach.coach_id)
        .filter(Coach.train_id == run.train_id, Coach.travel_class == travel_class)
        .order_by(Coach.coach_code, Seat.seat_number)
        .all()
    )

    occupied_ids = get_occupied_seat_ids(run_id, origin_seq, dest_seq)
    return [seat for seat in class_seats if seat.seat_id not in occupied_ids]
