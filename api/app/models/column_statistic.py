from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ColumnStatistic(db.Model):
    __tablename__ = "column_statistics"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    column_id = db.Column(UUID(as_uuid=True), db.ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)
    run_id = db.Column(UUID(as_uuid=True), db.ForeignKey("runs.id", ondelete="CASCADE"))

    null_fraction = db.Column(db.Float)
    distinct_count = db.Column(db.Integer)
    min_value = db.Column(db.String(255))
    max_value = db.Column(db.String(255))
    mean = db.Column(db.Float)

    column = db.relationship("Column", back_populates="statistics")

    def to_dict(self):
        return {
            "id": str(self.id),
            "run_id": str(self.run_id) if self.run_id else None,
            "null_fraction": self.null_fraction,
            "distinct_count": self.distinct_count,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "mean": self.mean
        }
