from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.dataset import Dataset
    from app.models.column_statistic import ColumnStatistic

class Column(db.Model):
    __tablename__ = "columns"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    data_type = db.Column(db.String(100))

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="columns")
    statistics: Mapped[list["ColumnStatistic"]] = relationship("ColumnStatistic", back_populates="column", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "data_type": self.data_type,
            "statistics": [stat.to_dict() for stat in self.statistics]
        }
