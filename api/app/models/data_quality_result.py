from ..extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .run import Run
    from .dataset import Dataset

class DataQualityResult(db.Model):
    __tablename__ = "data_quality_results"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = db.Column(UUID(as_uuid=True), db.ForeignKey("runs.id", ondelete="CASCADE"), nullable=False)
    dataset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    
    check_name = db.Column(db.String(255), nullable=False)
    success = db.Column(db.Boolean)
    observed_value = db.Column(db.String(255))
    expected_value = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    run = db.relationship("Run", back_populates="dq_results")
    dataset = db.relationship("Dataset", back_populates="dq_results")

    def to_dict(self):
        return {
            "id": str(self.id),
            "run_id": str(self.run_id),
            "dataset_id": str(self.dataset_id),
            "check_name": self.check_name,
            "success": self.success,
            "observed_value": self.observed_value,
            "expected_value": self.expected_value,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
