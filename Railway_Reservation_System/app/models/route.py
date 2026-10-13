"""
Route and TrainStop Models.
Represents fixed geographical tracks and ordered station sequences.
"""
from app.extensions import db


class Route(db.Model):
    __tablename__ = 'routes'

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    source_station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id', ondelete='RESTRICT'), nullable=False)
    destination_station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id', ondelete='RESTRICT'), nullable=False)
    total_distance_km = db.Column(db.Numeric(7, 2), nullable=False)

    # Relationships
    source_station = db.relationship('Station', foreign_keys=[source_station_id])
    destination_station = db.relationship('Station', foreign_keys=[destination_station_id])
    trains = db.relationship('Train', back_populates='route')
    stops = db.relationship('TrainStop', back_populates='route', order_by='TrainStop.stop_sequence', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'route_id': self.route_id,
            'route_code': self.route_code,
            'source_station': self.source_station.station_code if self.source_station else None,
            'destination_station': self.destination_station.station_code if self.destination_station else None,
            'total_distance_km': float(self.total_distance_km)
        }

    def __repr__(self):
        return f"<Route {self.route_code}>"


class TrainStop(db.Model):
    __tablename__ = 'train_stops'
    __table_args__ = (
        db.UniqueConstraint('route_id', 'stop_sequence', name='uq_route_stop_seq'),
        db.UniqueConstraint('route_id', 'station_id', name='uq_route_station'),
        db.CheckConstraint('stop_sequence > 0', name='chk_stop_seq_positive'),
        db.CheckConstraint('distance_from_source_km >= 0', name='chk_distance_nonneg'),
    )

    stop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id', ondelete='CASCADE'), nullable=False, index=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id', ondelete='RESTRICT'), nullable=False, index=True)
    stop_sequence = db.Column(db.Integer, nullable=False)
    distance_from_source_km = db.Column(db.Numeric(7, 2), nullable=False)
    arrival_time = db.Column(db.Time, nullable=True)     # NULL for first station
    departure_time = db.Column(db.Time, nullable=True)   # NULL for last station

    # Relationships
    route = db.relationship('Route', back_populates='stops')
    station = db.relationship('Station', back_populates='train_stops')

    def to_dict(self):
        return {
            'stop_id': self.stop_id,
            'route_id': self.route_id,
            'station_code': self.station.station_code if self.station else None,
            'station_name': self.station.station_name if self.station else None,
            'stop_sequence': self.stop_sequence,
            'distance_km': float(self.distance_from_source_km),
            'arrival_time': self.arrival_time.strftime('%H:%M') if self.arrival_time else '--',
            'departure_time': self.departure_time.strftime('%H:%M') if self.departure_time else '--'
        }

    def __repr__(self):
        return f"<TrainStop R{self.route_id} Seq{self.stop_sequence} Stn{self.station_id}>"
