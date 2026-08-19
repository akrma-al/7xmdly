from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if not username or len(username) < 3:
            errors.append("يجب أن يكون اسم المستخدم 3 أحرف على الأقل.")
        if not email or "@" not in email:
            errors.append("البريد الإلكتروني غير صالح.")
        if len(password) < 6:
            errors.append("يجب أن تكون كلمة المرور 6 أحرف على الأقل.")
        if password != confirm:
            errors.append("كلمتا المرور غير متطابقتين.")
        if User.query.filter_by(username=username).first():
            errors.append("اسم المستخدم مأخوذ بالفعل.")
        if User.query.filter_by(email=email).first():
            errors.append("البريد الإلكتروني مسجل بالفعل.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("auth/register.html")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("تم إنشاء الحساب بنجاح! يرجى تسجيل الدخول.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash("اسم المستخدم أو كلمة المرور غير صحيحة.", "error")
            return render_template("auth/login.html")

        login_user(user, remember=remember)
        flash(f"مرحباً بعودتك، {user.username}!", "success")
        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج بنجاح.", "info")
    return redirect(url_for("auth.login"))
