"""
Passenger Model.
Stores registered passenger profiles decoupled from booking transactions (3NF).
"""
from app.extensions import db


class Passenger(db.Model):
    __tablename__ = 'passengers'
    __table_args__ = (
        db.CheckConstraint('age > 0 AND age < 120', name='chk_passenger_age_valid'),
    )

    passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)       # MALE, FEMALE, OTHER
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    id_card_type = db.Column(db.String(20), nullable=False) # AADHAAR, PASSPORT, PAN, VOTER_ID
    id_card_number = db.Column(db.String(50), nullable=False)

    # Relationships
    bookings = db.relationship('Booking', back_populates='passenger', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'passenger_id': self.passenger_id,
            'full_name': self.full_name,
            'gender': self.gender,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'id_card_type': self.id_card_type,
            'id_card_number': self.id_card_number
        }

    def __repr__(self):
        return f"<Passenger {self.passenger_id} - {self.full_name}>"
