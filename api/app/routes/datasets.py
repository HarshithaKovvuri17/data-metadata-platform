from flask import Blueprint, request, jsonify
from app.extensions import db
from ..models import Dataset, Column, ColumnStatistic, DataQualityResult
from sqlalchemy.dialects.postgresql import UUID
import uuid

datasets_bp = Blueprint("datasets", __name__, url_prefix="/datasets")

@datasets_bp.route("", methods=["POST"])
def register_dataset():
    """
    Register a new dataset and its schema.
    Validates input, checks for existing URI, and saves to DB.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        name = data.get("name")
        uri = data.get("uri")
        if not name or not uri:
            return jsonify({"error": "Name and URI are required"}), 400

        # Check for existing dataset (Idempotency)
        dataset = Dataset.query.filter_by(uri=uri).first()
        if not dataset:
            # instantiate without kwargs and set fields manually
            dataset = Dataset()
            dataset.name = name
            dataset.uri = uri
            dataset.description = data.get("description")
            dataset.file_path = data.get("file_path")
            dataset.row_count = data.get("row_count")
            dataset.column_count = data.get("column_count")
            db.session.add(dataset)
            db.session.flush()
        else:
            # Update existing dataset
            dataset.name = name
            dataset.description = data.get("description")
            dataset.file_path = data.get("file_path")
            dataset.row_count = data.get("row_count")
            dataset.column_count = data.get("column_count")

        # Handle Columns
        schema = data.get("schema", [])
        for col_data in schema:
            col_name = col_data.get("name")
            column = Column.query.filter_by(dataset_id=dataset.id, name=col_name).first()
            if not column:
                # instantiate without kwargs and set fields manually
                column = Column()
                column.dataset_id = dataset.id
                column.name = col_name
                column.data_type = col_data.get("type")
                db.session.add(column)
            else:
                column.data_type = col_data.get("type")

        db.session.commit()

        return jsonify({
            "message": "Dataset registered successfully",
            "dataset_id": str(dataset.id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@datasets_bp.route("", methods=["GET"])
def get_all_datasets():
    datasets = Dataset.query.all()
    return jsonify([
        {
            "id": str(ds.id),
            "name": ds.name,
            "uri": ds.uri,
            "description": ds.description,
            "created_at": ds.created_at.isoformat() if ds.created_at else None
        } for ds in datasets
    ]), 200

@datasets_bp.route("/<uuid:dataset_id>", methods=["GET"])
def get_dataset_metadata(dataset_id):
    """
    Retrieve a dataset's full metadata profile.
    """
    ds = Dataset.query.get(dataset_id)

    if not ds:
        return jsonify({"error": "Dataset not found"}), 404

    return jsonify(ds.to_dict()), 200