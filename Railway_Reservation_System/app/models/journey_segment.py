"""
JourneySegment Model.
Represents the segment-wise allocation of a specific seat over a half-open station stop interval [start_stop_seq, end_stop_seq).
Core to the railway reservation business logic: supports seat reuse on non-overlapping segments and prevents conflicting allocations.
"""
from app.extensions import db


class JourneySegment(db.Model):
    __tablename__ = 'journey_segments'
    __table_args__ = (
        db.CheckConstraint('end_stop_seq > start_stop_seq', name='chk_segment_stop_order'),
        db.Index('idx_seat_run_alloc', 'run_id', 'seat_id', 'allocation_status'),
    )

    segment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete='CASCADE'), nullable=False, index=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seats.seat_id', ondelete='RESTRICT'), nullable=False, index=True)
    run_id = db.Column(db.Integer, db.ForeignKey('train_runs.run_id', ondelete='CASCADE'), nullable=False, index=True)
    start_stop_seq = db.Column(db.Integer, nullable=False)
    end_stop_seq = db.Column(db.Integer, nullable=False)
    allocation_status = db.Column(db.String(20), nullable=False, default='ACTIVE', index=True)  # ACTIVE, CANCELLED

    # Relationships
    booking = db.relationship('Booking', back_populates='journey_segments')
    seat = db.relationship('Seat', back_populates='journey_segments')
    train_run = db.relationship('TrainRun', back_populates='journey_segments')

    def overlaps_with(self, req_start: int, req_end: int) -> bool:
        """
        Interval overlap condition for half-open intervals [start, end):
        Existing [s, e) overlaps with Requested [r_start, r_end) iff:
        s < r_end AND r_start < e
        """
        if self.allocation_status != 'ACTIVE':
            return False
        return (self.start_stop_seq < req_end) and (req_start < self.end_stop_seq)

    def to_dict(self):
        return {
            'segment_id': self.segment_id,
            'booking_id': self.booking_id,
            'seat_id': self.seat_id,
            'seat_label': f"{self.seat.coach.coach_code}-{self.seat.seat_number}" if self.seat and self.seat.coach else str(self.seat_id),
            'run_id': self.run_id,
            'start_stop_seq': self.start_stop_seq,
            'end_stop_seq': self.end_stop_seq,
            'allocation_status': self.allocation_status
        }

    def __repr__(self):
        return f"<JourneySegment Seat{self.seat_id} Run{self.run_id} [{self.start_stop_seq}, {self.end_stop_seq}) {self.allocation_status}>"
