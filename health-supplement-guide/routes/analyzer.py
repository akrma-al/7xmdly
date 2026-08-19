from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from services.image_analyzer import analyze_medicine_image

analyzer_bp = Blueprint("analyzer", __name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}


@analyzer_bp.route("/", methods=["GET", "POST"])
@login_required
def analyze():
    result = None

    if request.method == "POST":
        if "medicine_image" not in request.files:
            flash("يرجى اختيار صورة للدواء.", "error")
            return render_template("analyzer.html", result=None)

        file = request.files["medicine_image"]

        if file.filename == "":
            flash("يرجى اختيار صورة للدواء.", "error")
            return render_template("analyzer.html", result=None)

        import os
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            flash("صيغة الملف غير مدعومة. يرجى استخدام JPG أو PNG أو WEBP.", "error")
            return render_template("analyzer.html", result=None)

        image_bytes = file.read()

        if len(image_bytes) > MAX_FILE_SIZE:
            flash("حجم الصورة كبير جداً. الحد الأقصى 10 ميغابايت.", "error")
            return render_template("analyzer.html", result=None)

        analysis = analyze_medicine_image(image_bytes, file.filename)

        if analysis["available"]:
            result = analysis
            flash(analysis["message"], "success")
        else:
            flash(analysis["message"], "error")
            result = analysis

    return render_template("analyzer.html", result=result)
