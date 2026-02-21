from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Run(db.Model):
    __tablename__ = "runs"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = db.Column(UUID(as_uuid=True), db.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50)) # START, COMPLETE, FAIL

    job = db.relationship("Job", back_populates="runs")
    dq_results = db.relationship("DataQualityResult", back_populates="run", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "job_id": str(self.job_id),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status
        }
