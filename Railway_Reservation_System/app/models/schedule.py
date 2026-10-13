"""
TrainRun (Schedule) Model.
Represents an individual physical run of a train on a specific calendar date.
Crucial for 3NF normalization: decouples static train definition from dated operational runs.
"""
from app.extensions import db


class TrainRun(db.Model):
    __tablename__ = 'train_runs'
    __table_args__ = (
        db.UniqueConstraint('train_id', 'run_date', name='uq_train_run_date'),
    )

    run_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id', ondelete='CASCADE'), nullable=False, index=True)
    run_date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='SCHEDULED')  # SCHEDULED, RUNNING, COMPLETED, CANCELLED

    # Relationships
    train = db.relationship('Train', back_populates='runs')
    bookings = db.relationship('Booking', back_populates='train_run', cascade='all, delete-orphan')
    journey_segments = db.relationship('JourneySegment', back_populates='train_run', cascade='all, delete-orphan')
    waitlists = db.relationship('Waitlist', back_populates='train_run', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'run_id': self.run_id,
            'train_id': self.train_id,
            'train_number': self.train.train_number if self.train else None,
            'train_name': self.train.train_name if self.train else None,
            'run_date': self.run_date.strftime('%Y-%m-%d'),
            'status': self.status
        }

    def __repr__(self):
        return f"<TrainRun {self.run_id} Train{self.train_id} on {self.run_date}>"
