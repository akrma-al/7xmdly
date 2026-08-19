from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from services.interaction_db import find_local_interactions
from services.interaction_ai import analyze_with_ai
from services.schedule import get_timing_conflicts

interactions_bp = Blueprint("interactions", __name__)


@interactions_bp.route("/")
@login_required
def check_interactions():
    user_supplements = current_user.supplements.all()
    supplement_names = []
    for us in user_supplements:
        if us.supplement:
            supplement_names.append(us.supplement.name)

    local_results = find_local_interactions(supplement_names)
    timing_conflicts = get_timing_conflicts(user_supplements)
    ai_results = None

    return render_template(
        "interactions.html",
        supplement_names=supplement_names,
        local_results=local_results,
        timing_conflicts=timing_conflicts,
        ai_results=ai_results,
        local_count=len(local_results),
        timing_count=len(timing_conflicts),
    )


@interactions_bp.route("/check_ai", methods=["POST"])
@login_required
def check_ai():
    user_supplements = current_user.supplements.all()
    supplement_names = []
    for us in user_supplements:
        if us.supplement:
            supplement_names.append(us.supplement.name)

    if not supplement_names:
        flash("أضف بعض المكملات أولاً قبل فحص التفاعلات.", "error")
        return render_template(
            "interactions.html",
            supplement_names=[],
            local_results=[],
            timing_conflicts=[],
            ai_results=None,
            local_count=0,
            timing_count=0,
        )

    local_results = find_local_interactions(supplement_names)
    timing_conflicts = get_timing_conflicts(user_supplements)
    ai_result = analyze_with_ai(supplement_names)

    return render_template(
        "interactions.html",
        supplement_names=supplement_names,
        local_results=local_results,
        timing_conflicts=timing_conflicts,
        ai_results=ai_result,
        local_count=len(local_results),
        timing_count=len(timing_conflicts),
    )
