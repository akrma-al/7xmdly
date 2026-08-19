import json
import os

from flask import Flask
from flask_login import LoginManager

from config import Config
from models import init_db, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "error"
    login_manager.login_message = "يجب تسجيل الدخول للوصول إلى هذه الصفحة."

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.supplements import supplements_bp
    from routes.interactions import interactions_bp
    from routes.schedule import schedule_bp
    from routes.analyzer import analyzer_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/")
    app.register_blueprint(supplements_bp, url_prefix="/supplements")
    app.register_blueprint(interactions_bp, url_prefix="/interactions")
    app.register_blueprint(schedule_bp, url_prefix="/schedule")
    app.register_blueprint(analyzer_bp, url_prefix="/analyzer")

    return app


def seed_data(app):
    """Populate the database with supplements and interactions from JSON."""
    from models.supplement import Supplement
    from models.interaction import Interaction

    with app.app_context():
        if Supplement.query.first() is not None:
            return

        data_path = os.path.join(os.path.dirname(__file__), "data", "supplements_db.json")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for s in data.get("supplements", []):
            supplement = Supplement(
                name=s["name"],
                category=s["category"],
                description=s.get("description", ""),
                default_dosage=s.get("default_dosage", ""),
                timing=s.get("timing", "morning"),
                benefits=s.get("benefits", ""),
                warnings=s.get("warnings", ""),
            )
            db.session.add(supplement)

        for i in data.get("interactions", []):
            interaction = Interaction(
                substance_a=i["substance_a"],
                substance_b=i["substance_b"],
                severity=i.get("severity", "low"),
                description=i.get("description", ""),
                recommendation=i.get("recommendation", ""),
            )
            db.session.add(interaction)

        db.session.commit()
        print(f"تم إضافة {len(data.get('supplements', []))} مكمل و {len(data.get('interactions', []))} تفاعل.")


if __name__ == "__main__":
    app = create_app()
    seed_data(app)
    app.run(debug=True, host="127.0.0.1", port=5001)
