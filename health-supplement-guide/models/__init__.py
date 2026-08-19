from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        from models.user import User
        from models.supplement import Supplement
        from models.user_supplement import UserSupplement
        from models.interaction import Interaction

        db.create_all()
