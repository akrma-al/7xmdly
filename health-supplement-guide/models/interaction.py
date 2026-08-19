from models import db


class Interaction(db.Model):
    __tablename__ = "interactions"

    id = db.Column(db.Integer, primary_key=True)
    substance_a = db.Column(db.String(100), nullable=False)
    substance_b = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), nullable=False, default="low")
    description = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "substance_a": self.substance_a,
            "substance_b": self.substance_b,
            "severity": self.severity,
            "description": self.description,
            "recommendation": self.recommendation,
        }
