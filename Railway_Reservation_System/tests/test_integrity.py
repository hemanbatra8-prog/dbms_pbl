"""
Database Integrity and Constraint Tests.
Validates PRIMARY KEY, FOREIGN KEY, UNIQUE, and CHECK constraints.
"""
import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from app.models.train import Train
from app.models.passenger import Passenger
from app.models.fare import FareRule
from app.models.route import TrainStop
from app.models.schedule import TrainRun


def test_unique_train_number_constraint(db_session):
    """Verify that inserting duplicate train numbers raises an IntegrityError."""
    t_dup = Train(
        train_number='22436',  # Already exists in seed data (Vande Bharat)
        train_name='Duplicate Express',
        train_type='Superfast Express',
        route_id=1
    )
    db_session.add(t_dup)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_invalid_foreign_key_rejected(db_session):
    """Verify that referencing a non-existent foreign key raises an IntegrityError."""
    invalid_run = TrainRun(
        train_id=99999,  # Does not exist
        run_date=date(2026, 11, 1),
        status='SCHEDULED'
    )
    db_session.add(invalid_run)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_passenger_age_check_constraint(db_session):
    """Verify CHECK constraint on passenger age (0 < age < 120)."""
    invalid_passenger = Passenger(
        full_name='Invalid Baby',
        gender='OTHER',
        age=150,  # Invalid: > 120
        email='invalid@example.com',
        phone='9999999999',
        id_card_type='AADHAAR',
        id_card_number='0000-0000-0000'
    )
    db_session.add(invalid_passenger)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_negative_fare_check_constraint(db_session):
    """Verify CHECK constraint prohibiting negative fare rules."""
    bad_fare = FareRule(
        train_type='Special',
        travel_class='3A',
        base_fare=Decimal('-100.00'),  # Negative fare
        rate_per_km=Decimal('1.00'),
        reservation_fee=Decimal('20.00')
    )
    db_session.add(bad_fare)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_duplicate_stop_sequence_rejected(db_session):
    """Verify UNIQUE constraint on (route_id, stop_sequence)."""
    # Route 1 already has stop_sequence 1 for NDLS
    dup_stop = TrainStop(
        route_id=1,
        station_id=5,
        stop_sequence=1,  # Duplicate sequence on Route 1
        distance_from_source_km=Decimal('10.00')
    )
    db_session.add(dup_stop)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
