"""
Fare Service.
Computes segment-based journey fares and refund calculations.
"""
from decimal import Decimal, ROUND_HALF_UP
from app.models.fare import FareRule
from app.models.route import TrainStop


def calculate_journey_fare(train_type: str, travel_class: str, origin_stop: TrainStop, dest_stop: TrainStop) -> Decimal:
    """
    Calculates fare based on distance between origin and destination stops,
    using FareRule (base_fare + rate_per_km * distance + reservation_fee).
    """
    fare_rule = FareRule.query.filter_by(train_type=train_type, travel_class=travel_class).first()
    
    # Fallback default rates if specific rule not found
    if not fare_rule:
        base_fare = Decimal('200.00')
        rate_per_km = Decimal('1.20')
        reservation_fee = Decimal('40.00')
    else:
        base_fare = Decimal(str(fare_rule.base_fare))
        rate_per_km = Decimal(str(fare_rule.rate_per_km))
        reservation_fee = Decimal(str(fare_rule.reservation_fee))

    distance = Decimal(str(dest_stop.distance_from_source_km)) - Decimal(str(origin_stop.distance_from_source_km))
    if distance <= Decimal('0.00'):
        distance = Decimal('50.00')  # Minimum segment baseline

    total = base_fare + (distance * rate_per_km) + reservation_fee
    # Round to 2 decimal places
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_cancellation_refund(total_fare: Decimal, booking_status: str) -> tuple[Decimal, Decimal]:
    """
    Calculates cancellation fee and refund amount.
    - Confirmed ticket: 20% cancellation deduction, 80% refund.
    - Waitlisted ticket: Flat Rs 30 clerkage fee deduction, rest refunded.
    Returns (cancellation_fee, refund_amount).
    """
    fare = Decimal(str(total_fare))
    if booking_status == 'CONFIRMED':
        cancellation_fee = (fare * Decimal('0.20')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        refund_amount = fare - cancellation_fee
    else:
        # Waitlisted or unconfirmed
        cancellation_fee = Decimal('30.00') if fare >= Decimal('30.00') else fare
        refund_amount = fare - cancellation_fee

    if refund_amount < Decimal('0.00'):
        refund_amount = Decimal('0.00')

    return cancellation_fee, refund_amount
