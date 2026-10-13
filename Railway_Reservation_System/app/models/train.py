"""
Train Model.
Represents train catalog definition (distinguished from individual dated runs).
"""
from app.extensions import db


class Train(db.Model):
    __tablename__ = 'trains'

    train_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_number = db.Column(db.String(10), unique=True, nullable=False, index=True)
    train_name = db.Column(db.String(100), nullable=False)
    train_type = db.Column(db.String(30), nullable=False)  # e.g., Rajdhani Express, Superfast, Mail/Express
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id', ondelete='RESTRICT'), nullable=False, index=True)

    # Relationships
    route = db.relationship('Route', back_populates='trains')
    coaches = db.relationship('Coach', back_populates='train', cascade='all, delete-orphan')
    runs = db.relationship('TrainRun', back_populates='train', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'train_id': self.train_id,
            'train_number': self.train_number,
            'train_name': self.train_name,
            'train_type': self.train_type,
            'route_id': self.route_id,
            'route_code': self.route.route_code if self.route else None
        }

    def __repr__(self):
        return f"<Train {self.train_number} - {self.train_name}>"
