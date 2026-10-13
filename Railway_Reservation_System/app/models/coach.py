"""
Coach and Seat Models.
Represents rolling stock carriages and individual seat units.
"""
from app.extensions import db


class Coach(db.Model):
    __tablename__ = 'coaches'
    __table_args__ = (
        db.UniqueConstraint('train_id', 'coach_code', name='uq_train_coach'),
    )

    coach_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id', ondelete='CASCADE'), nullable=False, index=True)
    coach_code = db.Column(db.String(10), nullable=False)   # e.g., 'B1', 'B2', 'A1', 'S1'
    travel_class = db.Column(db.String(10), nullable=False, index=True)  # '1A', '2A', '3A', 'SL', 'CC'
    total_seats = db.Column(db.Integer, nullable=False, default=72)

    # Relationships
    train = db.relationship('Train', back_populates='coaches')
    seats = db.relationship('Seat', back_populates='coach', cascade='all, delete-orphan', order_by='Seat.seat_number')

    def to_dict(self):
        return {
            'coach_id': self.coach_id,
            'train_id': self.train_id,
            'coach_code': self.coach_code,
            'travel_class': self.travel_class,
            'total_seats': self.total_seats
        }

    def __repr__(self):
        return f"<Coach {self.coach_code} ({self.travel_class}) Train{self.train_id}>"


class Seat(db.Model):
    __tablename__ = 'seats'
    __table_args__ = (
        db.UniqueConstraint('coach_id', 'seat_number', name='uq_coach_seat_number'),
        db.CheckConstraint('seat_number > 0', name='chk_seat_num_pos'),
    )

    seat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.coach_id', ondelete='CASCADE'), nullable=False, index=True)
    seat_number = db.Column(db.Integer, nullable=False)
    berth_type = db.Column(db.String(15), nullable=False)  # 'LOWER', 'MIDDLE', 'UPPER', 'SIDE LOWER', 'SIDE UPPER', 'WINDOW'

    # Relationships
    coach = db.relationship('Coach', back_populates='seats')
    journey_segments = db.relationship('JourneySegment', back_populates='seat', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'seat_id': self.seat_id,
            'coach_id': self.coach_id,
            'coach_code': self.coach.coach_code if self.coach else None,
            'travel_class': self.coach.travel_class if self.coach else None,
            'seat_number': self.seat_number,
            'berth_type': self.berth_type
        }

    def __repr__(self):
        return f"<Seat {self.coach.coach_code if self.coach else ''}-{self.seat_number} ({self.berth_type})>"
