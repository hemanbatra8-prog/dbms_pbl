"""
Seed Data Script.
Populates realistic Indian Railways operational data with routes, stops, coaches, seats,
and demonstrative bookings showcasing non-overlapping seat reuse and waitlists.
"""
from datetime import date, time, datetime
from decimal import Decimal
from app.extensions import db
from app.models.station import Station
from app.models.route import Route, TrainStop
from app.models.train import Train
from app.models.schedule import TrainRun
from app.models.coach import Coach, Seat
from app.models.passenger import Passenger
from app.models.fare import FareRule
from app.models.booking import Booking
from app.models.journey_segment import JourneySegment
from app.models.waitlist import Waitlist
from app.models.payment import Payment
from app.models.cancellation import Cancellation


def populate_seed_data(session=None):
    if session is None:
        session = db.session

    # Clear existing data in reverse FK dependency order
    session.query(Cancellation).delete()
    session.query(Payment).delete()
    session.query(Waitlist).delete()
    session.query(JourneySegment).delete()
    session.query(Booking).delete()
    session.query(Seat).delete()
    session.query(Coach).delete()
    session.query(TrainRun).delete()
    session.query(Train).delete()
    session.query(TrainStop).delete()
    session.query(Route).delete()
    session.query(FareRule).delete()
    session.query(Passenger).delete()
    session.query(Station).delete()
    session.commit()

    # 1. STATIONS
    stations_data = [
        ('NDLS', 'New Delhi', 'New Delhi', 'Delhi'),
        ('CNB', 'Kanpur Central', 'Kanpur', 'Uttar Pradesh'),
        ('PRYJ', 'Prayagraj Junction', 'Prayagraj', 'Uttar Pradesh'),
        ('BSB', 'Varanasi Junction', 'Varanasi', 'Uttar Pradesh'),
        ('DDU', 'Pt. Deen Dayal Upadhyaya Jn', 'Mughalsarai', 'Uttar Pradesh'),
        ('HWH', 'Howrah Junction', 'Kolkata', 'West Bengal'),
        ('MMCT', 'Mumbai Central', 'Mumbai', 'Maharashtra'),
        ('BRC', 'Vadodara Junction', 'Vadodara', 'Gujarat'),
        ('ADI', 'Ahmedabad Junction', 'Ahmedabad', 'Gujarat')
    ]
    stn_map = {}
    for code, name, city, state in stations_data:
        stn = Station(station_code=code, station_name=name, city=city, state=state)
        session.add(stn)
        session.flush()
        stn_map[code] = stn

    # 2. ROUTES
    # Route 1: New Delhi -> Varanasi (755 km)
    r1 = Route(
        route_code='RT-NDLS-BSB',
        source_station_id=stn_map['NDLS'].station_id,
        destination_station_id=stn_map['BSB'].station_id,
        total_distance_km=Decimal('755.00')
    )
    # Route 2: New Delhi -> Howrah (1450 km)
    r2 = Route(
        route_code='RT-NDLS-HWH',
        source_station_id=stn_map['NDLS'].station_id,
        destination_station_id=stn_map['HWH'].station_id,
        total_distance_km=Decimal('1450.00')
    )
    # Route 3: Mumbai -> Ahmedabad (492 km)
    r3 = Route(
        route_code='RT-MMCT-ADI',
        source_station_id=stn_map['MMCT'].station_id,
        destination_station_id=stn_map['ADI'].station_id,
        total_distance_km=Decimal('492.00')
    )
    session.add_all([r1, r2, r3])
    session.flush()

    # 3. TRAIN STOPS (Ordered sequence with stop_sequence > 0)
    stops_r1 = [
        (r1.route_id, stn_map['NDLS'].station_id, 1, Decimal('0.00'), None, time(6, 0)),
        (r1.route_id, stn_map['CNB'].station_id, 2, Decimal('440.00'), time(10, 8), time(10, 12)),
        (r1.route_id, stn_map['PRYJ'].station_id, 3, Decimal('635.00'), time(12, 8), time(12, 10)),
        (r1.route_id, stn_map['BSB'].station_id, 4, Decimal('755.00'), time(14, 0), None),
    ]
    stops_r2 = [
        (r2.route_id, stn_map['NDLS'].station_id, 1, Decimal('0.00'), None, time(16, 50)),
        (r2.route_id, stn_map['CNB'].station_id, 2, Decimal('440.00'), time(21, 35), time(21, 40)),
        (r2.route_id, stn_map['PRYJ'].station_id, 3, Decimal('635.00'), time(23, 43), time(23, 45)),
        (r2.route_id, stn_map['DDU'].station_id, 4, Decimal('790.00'), time(1, 47), time(1, 57)),
        (r2.route_id, stn_map['HWH'].station_id, 5, Decimal('1450.00'), time(9, 55), None),
    ]
    stops_r3 = [
        (r3.route_id, stn_map['MMCT'].station_id, 1, Decimal('0.00'), None, time(6, 20)),
        (r3.route_id, stn_map['BRC'].station_id, 2, Decimal('392.00'), time(11, 20), time(11, 25)),
        (r3.route_id, stn_map['ADI'].station_id, 3, Decimal('492.00'), time(12, 45), None),
    ]

    for rid, sid, seq, dist, arr, dep in stops_r1 + stops_r2 + stops_r3:
        session.add(TrainStop(
            route_id=rid,
            station_id=sid,
            stop_sequence=seq,
            distance_from_source_km=dist,
            arrival_time=arr,
            departure_time=dep
        ))
    session.flush()

    # 4. TRAINS
    t1 = Train(train_number='22436', train_name='Vande Bharat Express', train_type='Superfast Express', route_id=r1.route_id)
    t2 = Train(train_number='12301', train_name='Howrah Rajdhani Express', train_type='Rajdhani Express', route_id=r2.route_id)
    t3 = Train(train_number='12009', train_name='Mumbai - Ahmedabad Shatabdi', train_type='Shatabdi Express', route_id=r3.route_id)
    session.add_all([t1, t2, t3])
    session.flush()

    # 5. TRAIN RUNS (Operational calendar dates)
    run_dates = [date(2026, 10, 14), date(2026, 10, 15), date(2026, 10, 20)]
    train_runs = []
    for t in [t1, t2, t3]:
        for d in run_dates:
            tr = TrainRun(train_id=t.train_id, run_date=d, status='SCHEDULED')
            session.add(tr)
            train_runs.append(tr)
    session.flush()

    # 6. COACHES AND SEATS
    # Realistic compact coach capacities for demonstration and testing:
    # Vande Bharat: C1 (CC, 12 seats), E1 (1A, 6 seats)
    # Rajdhani: H1 (1A, 6 seats), A1 (2A, 8 seats), B1 (3A, 12 seats)
    # Shatabdi: C1 (CC, 12 seats), E1 (1A, 6 seats)
    coaches_config = [
        (t1.train_id, 'C1', 'CC', 12),
        (t1.train_id, 'E1', '1A', 6),
        (t2.train_id, 'H1', '1A', 6),
        (t2.train_id, 'A1', '2A', 8),
        (t2.train_id, 'B1', '3A', 12),
        (t3.train_id, 'C1', 'CC', 12),
        (t3.train_id, 'E1', '1A', 6)
    ]
    berth_cycle = ['LOWER', 'MIDDLE', 'UPPER', 'SIDE LOWER', 'SIDE UPPER', 'WINDOW', 'AISLE']
    seat_catalog = {}  # (coach_id, seat_number) -> Seat

    for tid, c_code, t_class, num_seats in coaches_config:
        coach = Coach(train_id=tid, coach_code=c_code, travel_class=t_class, total_seats=num_seats)
        session.add(coach)
        session.flush()
        for s_idx in range(1, num_seats + 1):
            berth = berth_cycle[(s_idx - 1) % len(berth_cycle)]
            st = Seat(coach_id=coach.coach_id, seat_number=s_idx, berth_type=berth)
            session.add(st)
            session.flush()
            seat_catalog[(coach.coach_id, s_idx)] = st

    # 7. FARE RULES
    fare_rules_data = [
        ('Rajdhani Express', '1A', Decimal('800.00'), Decimal('2.50'), Decimal('60.00')),
        ('Rajdhani Express', '2A', Decimal('500.00'), Decimal('1.80'), Decimal('50.00')),
        ('Rajdhani Express', '3A', Decimal('350.00'), Decimal('1.20'), Decimal('40.00')),
        ('Superfast Express', '1A', Decimal('700.00'), Decimal('2.20'), Decimal('60.00')),
        ('Superfast Express', 'CC', Decimal('250.00'), Decimal('1.10'), Decimal('40.00')),
        ('Superfast Express', '3A', Decimal('300.00'), Decimal('1.10'), Decimal('40.00')),
        ('Shatabdi Express', '1A', Decimal('750.00'), Decimal('2.30'), Decimal('60.00')),
        ('Shatabdi Express', 'CC', Decimal('280.00'), Decimal('1.15'), Decimal('40.00'))
    ]
    for t_type, t_class, base, rate, res_fee in fare_rules_data:
        session.add(FareRule(
            train_type=t_type,
            travel_class=t_class,
            base_fare=base,
            rate_per_km=rate,
            reservation_fee=res_fee
        ))
    session.flush()

    # 8. PASSENGERS
    passengers_data = [
        ('Aarav Sharma', 'MALE', 29, 'aarav.sharma@example.com', '9876543210', 'AADHAAR', '2345-6789-0123'),
        ('Priya Patel', 'FEMALE', 27, 'priya.patel@example.com', '9876543211', 'PASSPORT', 'L8923412'),
        ('Rajesh Kumar', 'MALE', 45, 'rajesh.kumar@example.com', '9876543212', 'AADHAAR', '3456-7890-1234'),
        ('Sunita Rao', 'FEMALE', 42, 'sunita.rao@example.com', '9876543213', 'PAN', 'ABCDE1234F'),
        ('Vikram Malhotra', 'MALE', 34, 'vikram.m@example.com', '9876543214', 'VOTER_ID', 'VTR892341'),
        ('Ananya Singh', 'FEMALE', 24, 'ananya.s@example.com', '9876543215', 'AADHAAR', '4567-8901-2345'),
        ('Rohan Gupta', 'MALE', 31, 'rohan.gupta@example.com', '9876543216', 'PASSPORT', 'Z1293847'),
        ('Meera Nair', 'FEMALE', 38, 'meera.nair@example.com', '9876543217', 'AADHAAR', '5678-9012-3456')
    ]
    passengers = []
    for name, gen, age, email, phone, id_type, id_num in passengers_data:
        p = Passenger(
            full_name=name, gender=gen, age=age, email=email,
            phone=phone, id_card_type=id_type, id_card_number=id_num
        )
        session.add(p)
        passengers.append(p)
    session.flush()

    # 9. BENCHMARK BOOKINGS & NON-OVERLAPPING SEAT REUSE DEMONSTRATION
    # Use TrainRun 1: Vande Bharat (22436) on 2026-10-14
    # Stops: 1: NDLS -> 2: CNB -> 3: PRYJ -> 4: BSB
    target_run = train_runs[0]
    c1_coach = Coach.query.filter_by(train_id=t1.train_id, coach_code='C1').first()
    seat_c1_1 = Seat.query.filter_by(coach_id=c1_coach.coach_id, seat_number=1).first()
    seat_c1_2 = Seat.query.filter_by(coach_id=c1_coach.coach_id, seat_number=2).first()
    seat_c1_3 = Seat.query.filter_by(coach_id=c1_coach.coach_id, seat_number=3).first()

    # Booking 1: Aarav Sharma books NDLS to CNB (stops 1 to 2) on Seat C1-1 [1, 2)
    b1 = Booking(
        pnr_number='2348912341',
        run_id=target_run.run_id,
        passenger_id=passengers[0].passenger_id,
        origin_station_id=stn_map['NDLS'].station_id,
        destination_station_id=stn_map['CNB'].station_id,
        origin_stop_seq=1,
        destination_stop_seq=2,
        travel_class='CC',
        booking_status='CONFIRMED',
        total_fare=Decimal('774.00'),
        booked_at=datetime(2026, 10, 10, 9, 30)
    )
    session.add(b1)
    session.flush()
    session.add(JourneySegment(
        booking_id=b1.booking_id,
        seat_id=seat_c1_1.seat_id,
        run_id=target_run.run_id,
        start_stop_seq=1,
        end_stop_seq=2,
        allocation_status='ACTIVE'
    ))
    session.add(Payment(
        booking_id=b1.booking_id,
        amount=Decimal('774.00'),
        payment_method='SIMULATED_UPI',
        transaction_reference='TXN-AARAV-001',
        payment_status='COMPLETED'
    ))

    # Booking 2: Priya Patel books CNB to BSB (stops 2 to 4) on SAME Seat C1-1 [2, 4)
    # Proves NON-OVERLAPPING REUSE OF SEAT C1-1!
    b2 = Booking(
        pnr_number='4569123842',
        run_id=target_run.run_id,
        passenger_id=passengers[1].passenger_id,
        origin_station_id=stn_map['CNB'].station_id,
        destination_station_id=stn_map['BSB'].station_id,
        origin_stop_seq=2,
        destination_stop_seq=4,
        travel_class='CC',
        booking_status='CONFIRMED',
        total_fare=Decimal('636.50'),
        booked_at=datetime(2026, 10, 10, 10, 15)
    )
    session.add(b2)
    session.flush()
    session.add(JourneySegment(
        booking_id=b2.booking_id,
        seat_id=seat_c1_1.seat_id,
        run_id=target_run.run_id,
        start_stop_seq=2,
        end_stop_seq=4,
        allocation_status='ACTIVE'
    ))
    session.add(Payment(
        booking_id=b2.booking_id,
        amount=Decimal('636.50'),
        payment_method='SIMULATED_CARD',
        transaction_reference='TXN-PRIYA-002',
        payment_status='COMPLETED'
    ))

    # Booking 3: Rajesh Kumar books NDLS to BSB (entire route stops 1 to 4) on Seat C1-2 [1, 4)
    b3 = Booking(
        pnr_number='6781293843',
        run_id=target_run.run_id,
        passenger_id=passengers[2].passenger_id,
        origin_station_id=stn_map['NDLS'].station_id,
        destination_station_id=stn_map['BSB'].station_id,
        origin_stop_seq=1,
        destination_stop_seq=4,
        travel_class='CC',
        booking_status='CONFIRMED',
        total_fare=Decimal('1120.50'),
        booked_at=datetime(2026, 10, 11, 14, 20)
    )
    session.add(b3)
    session.flush()
    session.add(JourneySegment(
        booking_id=b3.booking_id,
        seat_id=seat_c1_2.seat_id,
        run_id=target_run.run_id,
        start_stop_seq=1,
        end_stop_seq=4,
        allocation_status='ACTIVE'
    ))
    session.add(Payment(
        booking_id=b3.booking_id,
        amount=Decimal('1120.50'),
        payment_method='SIMULATED_UPI',
        transaction_reference='TXN-RAJESH-003',
        payment_status='COMPLETED'
    ))

    # Booking 4: Cancelled booking with refund audit record
    # Sunita Rao booked Seat C1-3 from NDLS to CNB, then cancelled
    b4 = Booking(
        pnr_number='8912384914',
        run_id=target_run.run_id,
        passenger_id=passengers[3].passenger_id,
        origin_station_id=stn_map['NDLS'].station_id,
        destination_station_id=stn_map['CNB'].station_id,
        origin_stop_seq=1,
        destination_stop_seq=2,
        travel_class='CC',
        booking_status='CANCELLED',
        total_fare=Decimal('774.00'),
        booked_at=datetime(2026, 10, 11, 16, 0)
    )
    session.add(b4)
    session.flush()
    session.add(JourneySegment(
        booking_id=b4.booking_id,
        seat_id=seat_c1_3.seat_id,
        run_id=target_run.run_id,
        start_stop_seq=1,
        end_stop_seq=2,
        allocation_status='CANCELLED'
    ))
    session.add(Payment(
        booking_id=b4.booking_id,
        amount=Decimal('774.00'),
        payment_method='SIMULATED_UPI',
        transaction_reference='TXN-SUNITA-004',
        payment_status='REFUNDED'
    ))
    # 20% cancellation fee = 154.80, refund = 619.20
    session.add(Cancellation(
        booking_id=b4.booking_id,
        cancellation_reason='Change in travel itinerary',
        cancellation_fee=Decimal('154.80'),
        refund_amount=Decimal('619.20'),
        refund_status='PROCESSED',
        cancelled_at=datetime(2026, 10, 12, 11, 30)
    ))

    # Booking 5: Waitlisted Booking
    # Vikram Malhotra booked 1A on target_run where 1A seats are filled
    b5 = Booking(
        pnr_number='9923481295',
        run_id=target_run.run_id,
        passenger_id=passengers[4].passenger_id,
        origin_station_id=stn_map['NDLS'].station_id,
        destination_station_id=stn_map['BSB'].station_id,
        origin_stop_seq=1,
        destination_stop_seq=4,
        travel_class='1A',
        booking_status='WAITLISTED',
        total_fare=Decimal('2421.00'),
        booked_at=datetime(2026, 10, 12, 18, 45)
    )
    session.add(b5)
    session.flush()
    session.add(Waitlist(
        booking_id=b5.booking_id,
        run_id=target_run.run_id,
        travel_class='1A',
        origin_stop_seq=1,
        destination_stop_seq=4,
        position=1,
        waitlist_status='WAITING'
    ))
    session.add(Payment(
        booking_id=b5.booking_id,
        amount=Decimal('2421.00'),
        payment_method='SIMULATED_NETBANKING',
        transaction_reference='TXN-VIKRAM-005',
        payment_status='COMPLETED'
    ))

    session.commit()
    print("Database successfully seeded with realistic Indian Railways sample data.")
