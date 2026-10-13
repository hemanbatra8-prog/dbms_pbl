"""
Cancellation and Refund Routes.
Handles ticket cancellation, refund processing, and automated waitlist promotion.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.booking import Booking
from app.services.cancellation_service import cancel_booking
from app.services.fare_service import calculate_cancellation_refund

cancel_bp = Blueprint('cancellations', __name__)


@cancel_bp.route('/cancel', methods=['GET'])
def cancel_search():
    pnr = request.args.get('pnr', '').strip()
    if pnr:
        booking = Booking.query.filter_by(pnr_number=pnr).first()
        if not booking:
            flash(f"PNR '{pnr}' not found.", "danger")
            return redirect(url_for('cancellations.cancel_search'))
        return redirect(url_for('cancellations.cancel_preview', pnr=pnr))
    return render_template('cancel_search.html')


@cancel_bp.route('/cancel/<pnr>', methods=['GET'])
def cancel_preview(pnr):
    booking = Booking.query.filter_by(pnr_number=pnr).first_or_404()
    if booking.booking_status == 'CANCELLED':
        flash("This booking is already cancelled.", "info")
        return redirect(url_for('bookings.booking_detail', pnr=pnr))

    fee, refund = calculate_cancellation_refund(booking.total_fare, booking.booking_status)
    return render_template('cancel_preview.html', booking=booking, fee=float(fee), refund=float(refund))


@cancel_bp.route('/cancel/<pnr>/confirm', methods=['POST'])
def cancel_process(pnr):
    booking = Booking.query.filter_by(pnr_number=pnr).first_or_404()
    reason = request.form.get('reason', 'Passenger voluntary cancellation').strip()

    try:
        result = cancel_booking(booking.booking_id, reason=reason)
        flash(result['message'], "success")
        return redirect(url_for('bookings.booking_detail', pnr=pnr))
    except Exception as e:
        flash(f"Failed to cancel booking: {str(e)}", "danger")
        return redirect(url_for('cancellations.cancel_preview', pnr=pnr))
