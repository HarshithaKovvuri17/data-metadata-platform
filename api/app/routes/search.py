from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app.extensions import db
from ..models import Dataset, Column

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods=["GET"])
def search_datasets():
    """
    Search datasets by name, description, or column name.
    """
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    query_like = f"%{query}%"

    results = (
        db.session.query(Dataset)
        .outerjoin(Column, Dataset.id == Column.dataset_id)
        .filter(
            or_(
                Dataset.name.ilike(query_like),
                Dataset.description.ilike(query_like),
                Column.name.ilike(query_like)
            )
        )
        .distinct()
        .all()
    )

    output = []
    for ds in results:
        output.append({
            "id": str(ds.id),
            "name": ds.name,
            "uri": ds.uri,
            "description": ds.description
        })

    return jsonify({
        "query": query,
        "results_count": len(output),
        "datasets": output
    }), 200
