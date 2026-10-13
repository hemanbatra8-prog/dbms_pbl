"""
Cancellation Service.
Implements ticket cancellation, refund enforcement, and automated waitlist promotion.
Guarantees transaction atomicity across booking, segment, payment, and waitlist tables.
"""
from decimal import Decimal
from app.extensions import db
from app.models.booking import Booking
from app.models.journey_segment import JourneySegment
from app.models.waitlist import Waitlist
from app.models.cancellation import Cancellation
from app.models.payment import Payment
from app.services.fare_service import calculate_cancellation_refund
from app.services.availability_service import get_available_seats


def cancel_booking(booking_id: int, reason: str = "Passenger voluntary cancellation") -> dict:
    """
    Cancels an existing booking, computes refund, and automatically promotes eligible waitlisted passengers.
    """
    booking = db.session.get(Booking, booking_id)
    if not booking:
        raise ValueError("Booking not found.")

    if booking.booking_status == 'CANCELLED':
        raise ValueError("Booking has already been cancelled. Cannot process duplicate cancellation.")

    run_id = booking.run_id
    travel_class = booking.travel_class
    orig_status = booking.booking_status

    try:
        # Calculate cancellation fee and refund based on policy
        cancellation_fee, refund_amount = calculate_cancellation_refund(booking.total_fare, orig_status)

        # 1. Update booking status
        booking.booking_status = 'CANCELLED'

        # 2. Free up journey segments if it was confirmed
        if orig_status == 'CONFIRMED':
            for seg in booking.journey_segments:
                seg.allocation_status = 'CANCELLED'

        # 3. Cancel waitlist entry if it was waitlisted
        if orig_status == 'WAITLISTED' and booking.waitlist_entry:
            booking.waitlist_entry.waitlist_status = 'CANCELLED'

        # 4. Record cancellation audit record
        cancellation = Cancellation(
            booking_id=booking.booking_id,
            cancellation_reason=reason,
            cancellation_fee=cancellation_fee,
            refund_amount=refund_amount,
            refund_status='PROCESSED'
        )
        db.session.add(cancellation)

        # 5. Update payment status
        if booking.payment:
            booking.payment.payment_status = 'REFUNDED'

        db.session.flush()

        # 6. Automated Waitlist Promotion:
        # If a confirmed seat was freed, attempt to promote the next eligible waitlisted passenger in queue
        promoted_pnr = None
        promoted_seat = None

        if orig_status == 'CONFIRMED':
            # Retrieve active waitlist entries for this run and class in strict FIFO order
            waiting_queue = (
                Waitlist.query
                .filter_by(run_id=run_id, travel_class=travel_class, waitlist_status='WAITING')
                .order_by(Waitlist.position.asc())
                .all()
            )

            for candidate_wl in waiting_queue:
                # Re-verify full segment availability for this candidate's journey
                candidate_avail_seats = get_available_seats(
                    run_id,
                    travel_class,
                    candidate_wl.origin_stop_seq,
                    candidate_wl.destination_stop_seq
                )

                if len(candidate_avail_seats) > 0:
                    assigned_seat = candidate_avail_seats[0]

                    # Create active segment for promoted passenger
                    promo_seg = JourneySegment(
                        booking_id=candidate_wl.booking_id,
                        seat_id=assigned_seat.seat_id,
                        run_id=run_id,
                        start_stop_seq=candidate_wl.origin_stop_seq,
                        end_stop_seq=candidate_wl.destination_stop_seq,
                        allocation_status='ACTIVE'
                    )
                    db.session.add(promo_seg)

                    # Update candidate booking & waitlist status
                    candidate_wl.waitlist_status = 'PROMOTED'
                    candidate_wl.booking.booking_status = 'CONFIRMED'

                    promoted_pnr = candidate_wl.booking.pnr_number
                    promoted_seat = f"{assigned_seat.coach.coach_code}-{assigned_seat.seat_number} ({assigned_seat.berth_type})"
                    break  # One seat freed promotes one eligible candidate for this segment

        db.session.commit()

        return {
            'pnr_number': booking.pnr_number,
            'cancellation_id': cancellation.cancellation_id,
            'original_fare': float(booking.total_fare),
            'cancellation_fee': float(cancellation_fee),
            'refund_amount': float(refund_amount),
            'promoted_pnr': promoted_pnr,
            'promoted_seat': promoted_seat,
            'message': f"Booking {booking.pnr_number} successfully cancelled. Refund of ₹{refund_amount} processed."
                       + (f" Waitlisted passenger {promoted_pnr} promoted to {promoted_seat}." if promoted_pnr else "")
        }

    except Exception as e:
        db.session.rollback()
        raise e
