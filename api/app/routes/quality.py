from flask import Blueprint, request, jsonify

from app.extensions import db
from ..models import DataQualityResult, Dataset, Run

quality_bp = Blueprint("quality", __name__)


@quality_bp.route("/runs/<uuid:run_id>/dq_results", methods=["POST"])
def store_run_quality_results(run_id):
    """
    Store data quality results for a specific run.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        run = Run.query.get(run_id)
        if not run:
            return jsonify({"error": "Run not found"}), 404

        dataset_uri = data.get("dataset_uri")
        dataset = Dataset.query.filter_by(uri=dataset_uri).first()
        if not dataset:
            return jsonify({"error": f"Dataset with URI {dataset_uri} not found"}), 404

        results = data.get("results", [])
        for r in results:
            dq_record = DataQualityResult()
            # set attributes explicitly since the model’s __init__
            # does not declare those keyword args
            dq_record.run_id = run.id
            dq_record.dataset_id = dataset.id
            dq_record.check_name = r.get("check_name")
            dq_record.success = r.get("success")
            dq_record.observed_value = str(r.get("observed_value"))
            dq_record.expected_value = str(r.get("expected_value"))
            db.session.add(dq_record)

        db.session.commit()
        return jsonify({"message": "Data quality results stored successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
