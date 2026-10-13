"""
FareRule Model.
Stores deterministic fare calculation parameters by train type and travel class.
"""
from app.extensions import db


class FareRule(db.Model):
    __tablename__ = 'fare_rules'
    __table_args__ = (
        db.UniqueConstraint('train_type', 'travel_class', name='uq_train_type_class'),
        db.CheckConstraint('base_fare >= 0', name='chk_base_fare_nonneg'),
        db.CheckConstraint('rate_per_km >= 0', name='chk_rate_km_nonneg'),
        db.CheckConstraint('reservation_fee >= 0', name='chk_res_fee_nonneg'),
    )

    fare_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_type = db.Column(db.String(30), nullable=False)   # Rajdhani Express, Superfast, Mail/Express
    travel_class = db.Column(db.String(10), nullable=False) # 1A, 2A, 3A, SL, CC
    base_fare = db.Column(db.Numeric(10, 2), nullable=False)
    rate_per_km = db.Column(db.Numeric(6, 2), nullable=False)
    reservation_fee = db.Column(db.Numeric(6, 2), nullable=False, default=40.00)

    def to_dict(self):
        return {
            'fare_id': self.fare_id,
            'train_type': self.train_type,
            'travel_class': self.travel_class,
            'base_fare': float(self.base_fare),
            'rate_per_km': float(self.rate_per_km),
            'reservation_fee': float(self.reservation_fee)
        }

    def __repr__(self):
        return f"<FareRule {self.train_type} {self.travel_class}: Base={self.base_fare}>"
