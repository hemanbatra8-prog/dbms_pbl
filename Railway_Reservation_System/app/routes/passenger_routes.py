"""
Passenger Management Routes.
Handles passenger profile registration, listings, and updates.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.passenger import Passenger

passenger_bp = Blueprint('passengers', __name__)


@passenger_bp.route('/passengers', methods=['GET', 'POST'])
def manage_passengers():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        gender = request.form.get('gender', 'MALE')
        age_str = request.form.get('age', '25')
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        id_card_type = request.form.get('id_card_type', 'AADHAAR')
        id_card_number = request.form.get('id_card_number', '').strip()

        try:
            age = int(age_str)
            if age <= 0 or age >= 120:
                raise ValueError("Age must be between 1 and 119.")
            if not full_name or not email or not phone or not id_card_number:
                raise ValueError("All fields are mandatory.")

            passenger = Passenger(
                full_name=full_name,
                gender=gender,
                age=age,
                email=email,
                phone=phone,
                id_card_type=id_card_type,
                id_card_number=id_card_number
            )
            db.session.add(passenger)
            db.session.commit()
            flash(f"Passenger {full_name} registered successfully!", "success")
            return redirect(url_for('passengers.manage_passengers'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error registering passenger: {str(e)}", "danger")

    passengers = Passenger.query.order_by(Passenger.passenger_id.desc()).all()
    return render_template('passengers.html', passengers=passengers)
