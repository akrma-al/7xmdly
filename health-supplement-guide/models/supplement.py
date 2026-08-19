from models import db


class Supplement(db.Model):
    __tablename__ = "supplements"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    default_dosage = db.Column(db.String(50), nullable=False, default="")
    timing = db.Column(db.String(100), nullable=False, default="morning")
    benefits = db.Column(db.Text, nullable=False, default="")
    warnings = db.Column(db.Text, nullable=False, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "default_dosage": self.default_dosage,
            "timing": self.timing,
            "benefits": self.benefits,
            "warnings": self.warnings,
        }
