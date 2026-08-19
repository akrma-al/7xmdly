from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.supplement import Supplement
from models.user_supplement import UserSupplement

supplements_bp = Blueprint("supplements", __name__)


@supplements_bp.route("/")
@login_required
def list_supplements():
    user_supplements = current_user.supplements.all()
    all_supplements = Supplement.query.order_by(Supplement.name).all()
    user_sup_ids = [us.supplement_id for us in user_supplements]
    available = [s for s in all_supplements if s.id not in user_sup_ids]

    return render_template(
        "supplements.html",
        user_supplements=user_supplements,
        all_supplements=all_supplements,
        available_supplements=available,
    )


@supplements_bp.route("/add", methods=["POST"])
@login_required
def add_supplement():
    supplement_id = request.form.get("supplement_id", type=int)
    custom_dosage = request.form.get("custom_dosage", "").strip()
    notes = request.form.get("notes", "").strip()

    if not supplement_id:
        flash("يرجى اختيار مكمل غذائي.", "error")
        return redirect(url_for("supplements.list_supplements"))

    existing = UserSupplement.query.filter_by(
        user_id=current_user.id, supplement_id=supplement_id
    ).first()

    if existing:
        flash("هذا المكمل مُضاف بالفعل في قائمتك.", "error")
        return redirect(url_for("supplements.list_supplements"))

    us = UserSupplement(
        user_id=current_user.id,
        supplement_id=supplement_id,
        custom_dosage=custom_dosage if custom_dosage else None,
        notes=notes if notes else None,
    )
    db.session.add(us)
    db.session.commit()
    flash("تم إضافة المكمل بنجاح!", "success")
    return redirect(url_for("supplements.list_supplements"))


@supplements_bp.route("/add_custom", methods=["POST"])
@login_required
def add_custom():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    dosage = request.form.get("dosage", "").strip()
    timing = request.form.get("timing", "morning").strip()

    if not name:
        flash("اسم المكمل مطلوب.", "error")
        return redirect(url_for("supplements.list_supplements"))

    if not category:
        category = "أخرى"

    existing = Supplement.query.filter(
        Supplement.name.ilike(name)
    ).first()

    if existing:
        supplement = existing
    else:
        supplement = Supplement(
            name=name,
            category=category,
            description=description or f"مكمل مخصص: {name}",
            default_dosage=dosage or "اتبع التعليمات على العلبة",
            timing=timing or "morning",
        )
        db.session.add(supplement)
        db.session.flush()

    already_added = UserSupplement.query.filter_by(
        user_id=current_user.id, supplement_id=supplement.id
    ).first()

    if already_added:
        flash(f"{name} مُضاف بالفعل في قائمتك.", "error")
        return redirect(url_for("supplements.list_supplements"))

    us = UserSupplement(
        user_id=current_user.id,
        supplement_id=supplement.id,
        custom_dosage=dosage if dosage else None,
        notes=description if description else None,
    )
    db.session.add(us)
    db.session.commit()
    flash(f"تم إضافة {name} بنجاح!", "success")
    return redirect(url_for("supplements.list_supplements"))


@supplements_bp.route("/remove/<int:us_id>", methods=["POST"])
@login_required
def remove_supplement(us_id):
    us = UserSupplement.query.filter_by(id=us_id, user_id=current_user.id).first_or_404()
    db.session.delete(us)
    db.session.commit()
    flash("تم إزالة المكمل.", "info")
    return redirect(url_for("supplements.list_supplements"))


@supplements_bp.route("/update/<int:us_id>", methods=["POST"])
@login_required
def update_supplement(us_id):
    us = UserSupplement.query.filter_by(id=us_id, user_id=current_user.id).first_or_404()
    custom_dosage = request.form.get("custom_dosage", "").strip()
    notes = request.form.get("notes", "").strip()

    us.custom_dosage = custom_dosage if custom_dosage else None
    us.notes = notes if notes else None
    db.session.commit()
    flash("تم تحديث المكمل بنجاح.", "success")
    return redirect(url_for("supplements.list_supplements"))
