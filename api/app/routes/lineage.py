from flask import Blueprint, jsonify

from ..models import LineageEdge, Dataset
from app.extensions import db

lineage_bp = Blueprint("lineage", __name__)

@lineage_bp.route("/datasets/<uuid:dataset_id>/lineage", methods=["GET"])
def get_lineage(dataset_id):
    """
    Get upstream and downstream lineage for a dataset.
    """
    # Upstream: edges where target_dataset_id is this dataset
    upstream_edges = LineageEdge.query.filter_by(target_dataset_id=dataset_id).all()
    # Downstream: edges where source_dataset_id is this dataset
    downstream_edges = LineageEdge.query.filter_by(source_dataset_id=dataset_id).all()

    upstream = []
    for edge in upstream_edges:
        ds = Dataset.query.get(edge.source_dataset_id)
        if ds:
            upstream.append({
                "id": str(ds.id),
                "name": ds.name,
                "edge_type": edge.edge_type
            })

    downstream = []
    for edge in downstream_edges:
        ds = Dataset.query.get(edge.target_dataset_id)
        if ds:
            downstream.append({
                "id": str(ds.id),
                "name": ds.name,
                "edge_type": edge.edge_type
            })

    return jsonify({
        "dataset_id": str(dataset_id),
        "upstream": upstream,
        "downstream": downstream
    }), 200

