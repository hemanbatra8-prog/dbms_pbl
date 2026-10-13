"""
Pytest configuration and shared test fixtures.
"""
import pytest
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from database.seed_data import populate_seed_data


@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application."""
    app = create_app(TestingConfig)
    return app


@pytest.fixture(scope='function')
def db_session(app):
    """Creates a fresh database schema for every test function."""
    with app.app_context():
        db.create_all()
        populate_seed_data(db.session)
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app, db_session):
    """Flask test client."""
    return app.test_client()
