"""
Application Entry Point.
Runs the Railway Ticket Reservation and Journey Management System.
"""
import os
import sys
from pathlib import Path

# Ensure application path is in python sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import create_app
from app.extensions import db
from database.seed_data import populate_seed_data

app = create_app()

def initialize_database():
    """Initializes tables and populates seed data if empty."""
    with app.app_context():
        db.create_all()
        from app.models.station import Station
        if Station.query.count() == 0:
            print("Database empty. Initializing schema and seeding benchmark railway data...")
            populate_seed_data(db.session)
            print("Database successfully initialized!")

if __name__ == '__main__':
    initialize_database()
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Railway Reservation System on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
