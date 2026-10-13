"""
Station Model.
Represents a physical railway station.
"""
from app.extensions import db


class Station(db.Model):
    __tablename__ = 'stations'

    station_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    station_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)

    # Relationships
    train_stops = db.relationship('TrainStop', back_populates='station', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'station_id': self.station_id,
            'station_code': self.station_code,
            'station_name': self.station_name,
            'city': self.city,
            'state': self.state
        }

    def __repr__(self):
        return f"<Station {self.station_code} - {self.station_name}>"
