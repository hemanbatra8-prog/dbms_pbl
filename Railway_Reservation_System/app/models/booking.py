"""
Booking Model.
Represents a ticket reservation transaction for a passenger on a specific train run.
"""
from datetime import datetime
from app.extensions import db


class Booking(db.Model):
    __tablename__ = 'bookings'
    __table_args__ = (
        db.CheckConstraint('destination_stop_seq > origin_stop_seq', name='chk_booking_stop_order'),
        db.CheckConstraint('total_fare >= 0', name='chk_total_fare_nonneg'),
    )

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pnr_number = db.Column(db.String(12), unique=True, nullable=False, index=True)
    run_id = db.Column(db.Integer, db.ForeignKey('train_runs.run_id', ondelete='RESTRICT'), nullable=False, index=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id', ondelete='RESTRICT'), nullable=False, index=True)
    origin_station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id', ondelete='RESTRICT'), nullable=False)
    destination_station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id', ondelete='RESTRICT'), nullable=False)
    origin_stop_seq = db.Column(db.Integer, nullable=False)
    destination_stop_seq = db.Column(db.Integer, nullable=False)
    travel_class = db.Column(db.String(10), nullable=False)
    booking_status = db.Column(db.String(20), nullable=False, default='CONFIRMED', index=True)  # CONFIRMED, WAITLISTED, CANCELLED
    total_fare = db.Column(db.Numeric(10, 2), nullable=False)
    booked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    train_run = db.relationship('TrainRun', back_populates='bookings')
    passenger = db.relationship('Passenger', back_populates='bookings')
    origin_station = db.relationship('Station', foreign_keys=[origin_station_id])
    destination_station = db.relationship('Station', foreign_keys=[destination_station_id])
    journey_segments = db.relationship('JourneySegment', back_populates='booking', cascade='all, delete-orphan')
    waitlist_entry = db.relationship('Waitlist', back_populates='booking', uselist=False, cascade='all, delete-orphan')
    payment = db.relationship('Payment', back_populates='booking', uselist=False, cascade='all, delete-orphan')
    cancellation = db.relationship('Cancellation', back_populates='booking', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        allocated_seat = None
        for seg in self.journey_segments:
            if seg.allocation_status == 'ACTIVE' and seg.seat:
                allocated_seat = f"{seg.seat.coach.coach_code}-{seg.seat.seat_number} ({seg.seat.berth_type})"
                break

        return {
            'booking_id': self.booking_id,
            'pnr_number': self.pnr_number,
            'train_number': self.train_run.train.train_number if self.train_run and self.train_run.train else None,
            'train_name': self.train_run.train.train_name if self.train_run and self.train_run.train else None,
            'run_date': self.train_run.run_date.strftime('%Y-%m-%d') if self.train_run else None,
            'passenger_name': self.passenger.full_name if self.passenger else None,
            'origin': self.origin_station.station_code if self.origin_station else None,
            'destination': self.destination_station.station_code if self.destination_station else None,
            'travel_class': self.travel_class,
            'booking_status': self.booking_status,
            'total_fare': float(self.total_fare),
            'booked_at': self.booked_at.strftime('%Y-%m-%d %H:%M:%S'),
            'seat_allocation': allocated_seat or ('WAITLISTED' if self.booking_status == 'WAITLISTED' else 'NONE')
        }

    def __repr__(self):
        return f"<Booking PNR={self.pnr_number} Status={self.booking_status}>"
