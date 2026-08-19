from models import db


class UserSupplement(db.Model):
    __tablename__ = "user_supplements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    supplement_id = db.Column(db.Integer, db.ForeignKey("supplements.id"), nullable=False)
    custom_dosage = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True, default="")

    supplement = db.relationship("Supplement", backref="user_entries")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "supplement_id": self.supplement_id,
            "custom_dosage": self.custom_dosage,
            "notes": self.notes,
            "supplement": self.supplement.to_dict() if self.supplement else None,
        }
