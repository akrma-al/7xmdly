from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    user_supplements = current_user.supplements.all()
    supplement_count = len(user_supplements)
    categories = set()
    for us in user_supplements:
        if us.supplement:
            categories.add(us.supplement.category)

    return render_template(
        "dashboard.html",
        user_supplements=user_supplements,
        supplement_count=supplement_count,
        category_count=len(categories),
    )
