from flask import Blueprint, render_template, request
from ..models import Dataset, Column, ColumnStatistic, DataQualityResult
from ..extensions import db

catalog_bp = Blueprint("catalog", __name__)

@catalog_bp.route("/")
def home():
    return render_template("home.html")

@catalog_bp.route("/catalog")
def catalog():
    datasets = Dataset.query.all()
    return render_template("datasets.html", datasets=datasets)

@catalog_bp.route("/catalog/<uuid:dataset_id>")
def dataset_detail(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    columns = Column.query.filter_by(dataset_id=dataset.id).all()
    dq_results = DataQualityResult.query.filter_by(dataset_id=dataset.id).order_by(DataQualityResult.timestamp.desc()).all()

    return render_template(
        "dataset_detail.html",
        dataset=dataset,
        columns=columns,
        dq_results=dq_results
    )

@catalog_bp.route("/search")
def search():
    query = request.args.get("q", "")
    datasets = Dataset.query.filter(Dataset.name.ilike(f"%{query}%")).all()
    return render_template("search.html", datasets=datasets, query=query)