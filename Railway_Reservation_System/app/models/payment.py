"""
Payment Model.
Simulates payment transactions with financial precision (DECIMAL).
Separated from booking records for 3NF compliance and auditability.
"""
from datetime import datetime
from app.extensions import db


class Payment(db.Model):
    __tablename__ = 'payments'
    __table_args__ = (
        db.CheckConstraint('amount >= 0', name='chk_payment_amount_nonneg'),
    )

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete='CASCADE'), nullable=False, index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(30), nullable=False, default='SIMULATED_UPI')  # SIMULATED_UPI, CARD, NETBANKING
    transaction_reference = db.Column(db.String(60), unique=True, nullable=False, index=True)
    payment_status = db.Column(db.String(20), nullable=False, default='COMPLETED')  # COMPLETED, REFUNDED, FAILED
    paid_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    booking = db.relationship('Booking', back_populates='payment')

    def to_dict(self):
        return {
            'payment_id': self.payment_id,
            'booking_id': self.booking_id,
            'pnr_number': self.booking.pnr_number if self.booking else None,
            'amount': float(self.amount),
            'payment_method': self.payment_method,
            'transaction_reference': self.transaction_reference,
            'payment_status': self.payment_status,
            'paid_at': self.paid_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<Payment Ref={self.transaction_reference} Amt={self.amount} Status={self.payment_status}>"
