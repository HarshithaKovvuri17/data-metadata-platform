from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)

    runs = db.relationship("Run", back_populates="job", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description
        }
