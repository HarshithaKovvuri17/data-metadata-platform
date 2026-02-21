from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dataset import Dataset
    from .run import Run

class LineageEdge(db.Model):
    __tablename__ = "lineage_edges"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_dataset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("datasets.id", ondelete="CASCADE"))
    target_dataset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("datasets.id", ondelete="CASCADE"))
    job_run_id = db.Column(UUID(as_uuid=True), db.ForeignKey("runs.id", ondelete="CASCADE"))
    edge_type = db.Column(db.String(50)) # e.g. INPUT_TO_OUTPUT

    source_dataset = db.relationship("Dataset", foreign_keys=[source_dataset_id])
    target_dataset = db.relationship("Dataset", foreign_keys=[target_dataset_id])
    run = db.relationship("Run")

    def to_dict(self):
        return {
            "id": str(self.id),
            "source_dataset_id": str(self.source_dataset_id) if self.source_dataset_id else None,
            "target_dataset_id": str(self.target_dataset_id) if self.target_dataset_id else None,
            "job_run_id": str(self.job_run_id) if self.job_run_id else None,
            "edge_type": self.edge_type
        }
