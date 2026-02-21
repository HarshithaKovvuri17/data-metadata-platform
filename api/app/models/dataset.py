from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
from typing import List, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.column import Column
    from app.models.data_quality_result import DataQualityResult

class Dataset(db.Model):
    __tablename__ = "datasets"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    uri = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    row_count = db.Column(db.Integer)
    column_count = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    columns: Mapped[List["Column"]] = relationship("Column", back_populates="dataset", cascade="all, delete-orphan")
    dq_results: Mapped[List["DataQualityResult"]] = relationship("DataQualityResult", back_populates="dataset", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "uri": self.uri,
            "description": self.description,
            "file_path": self.file_path,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "columns": [col.to_dict() for col in self.columns],
            "data_quality_results": [dq.to_dict() for dq in self.dq_results]
        }
