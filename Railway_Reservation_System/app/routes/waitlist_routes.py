"""
Waitlist Management Routes.
Displays live queue positions and promotion logs.
"""
from flask import Blueprint, render_template
from app.models.waitlist import Waitlist

waitlist_bp = Blueprint('waitlist', __name__)


@waitlist_bp.route('/waitlist')
def view_waitlist():
    entries = Waitlist.query.order_by(Waitlist.run_id, Waitlist.travel_class, Waitlist.position).all()
    return render_template('waitlist.html', entries=entries)
