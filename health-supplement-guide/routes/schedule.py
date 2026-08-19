from flask import Blueprint, render_template
from flask_login import login_required, current_user
from services.schedule import generate_daily_schedule, get_timing_conflicts

schedule_bp = Blueprint("schedule", __name__)


@schedule_bp.route("/")
@login_required
def daily_schedule():
    user_supplements = current_user.supplements.all()
    schedule = generate_daily_schedule(user_supplements)
    conflicts = get_timing_conflicts(user_supplements)

    total_items = sum(slot["count"] for slot in schedule)

    return render_template(
        "schedule.html",
        schedule=schedule,
        conflicts=conflicts,
        total_items=total_items,
    )
