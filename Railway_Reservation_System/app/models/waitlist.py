"""
Waitlist Model.
Represents queued reservation requests when all seats in a class for a journey segment are exhausted.
Supports ordered FIFO priority queue and automated promotion upon segment cancellation.
"""
from datetime import datetime
from app.extensions import db


class Waitlist(db.Model):
    __tablename__ = 'waitlists'
    __table_args__ = (
        db.CheckConstraint('position > 0', name='chk_waitlist_pos_pos'),
        db.CheckConstraint('destination_stop_seq > origin_stop_seq', name='chk_waitlist_stop_order'),
        db.Index('idx_waitlist_run_class_pos', 'run_id', 'travel_class', 'position'),
    )

    waitlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete='CASCADE'), nullable=False, index=True)
    run_id = db.Column(db.Integer, db.ForeignKey('train_runs.run_id', ondelete='CASCADE'), nullable=False, index=True)
    travel_class = db.Column(db.String(10), nullable=False)
    origin_stop_seq = db.Column(db.Integer, nullable=False)
    destination_stop_seq = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    waitlist_status = db.Column(db.String(20), nullable=False, default='WAITING', index=True)  # WAITING, PROMOTED, CANCELLED
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    booking = db.relationship('Booking', back_populates='waitlist_entry')
    train_run = db.relationship('TrainRun', back_populates='waitlists')

    def to_dict(self):
        return {
            'waitlist_id': self.waitlist_id,
            'pnr_number': self.booking.pnr_number if self.booking else None,
            'passenger_name': self.booking.passenger.full_name if self.booking and self.booking.passenger else None,
            'train_number': self.train_run.train.train_number if self.train_run and self.train_run.train else None,
            'run_date': self.train_run.run_date.strftime('%Y-%m-%d') if self.train_run else None,
            'travel_class': self.travel_class,
            'position': self.position,
            'waitlist_status': self.waitlist_status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<Waitlist PNR={self.booking.pnr_number if self.booking else '?'} Pos={self.position} Status={self.waitlist_status}>"
