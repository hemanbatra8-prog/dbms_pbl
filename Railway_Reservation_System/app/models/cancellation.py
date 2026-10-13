"""
Cancellation Model.
Audits ticket cancellations, fee deductions, and refund calculations.
Preserves historical records for reconciliation rather than deleting data rows.
"""
from datetime import datetime
from app.extensions import db


class Cancellation(db.Model):
    __tablename__ = 'cancellations'
    __table_args__ = (
        db.CheckConstraint('cancellation_fee >= 0', name='chk_cancel_fee_nonneg'),
        db.CheckConstraint('refund_amount >= 0', name='chk_refund_amt_nonneg'),
    )

    cancellation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete='RESTRICT'), unique=True, nullable=False, index=True)
    cancellation_reason = db.Column(db.String(255), nullable=False)
    cancellation_fee = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    refund_amount = db.Column(db.Numeric(10, 2), nullable=False)
    refund_status = db.Column(db.String(20), nullable=False, default='PROCESSED')  # PROCESSED, PENDING
    cancelled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    booking = db.relationship('Booking', back_populates='cancellation')

    def to_dict(self):
        return {
            'cancellation_id': self.cancellation_id,
            'booking_id': self.booking_id,
            'pnr_number': self.booking.pnr_number if self.booking else None,
            'cancellation_reason': self.cancellation_reason,
            'cancellation_fee': float(self.cancellation_fee),
            'refund_amount': float(self.refund_amount),
            'refund_status': self.refund_status,
            'cancelled_at': self.cancelled_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<Cancellation Booking={self.booking_id} Refund={self.refund_amount}>"
