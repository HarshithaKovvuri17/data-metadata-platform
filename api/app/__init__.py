from flask import Flask
from .config import Config
from .extensions import db, ma


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # import models AFTER db init (VERY IMPORTANT)
    with app.app_context():
        from .models import Dataset, Column, ColumnStatistic, DataQualityResult, Job, Run, LineageEdge
        db.create_all()


    # register routes
    from .routes.health import health_bp
    from .routes.datasets import datasets_bp
    from .routes.search import search_bp
    from .routes.quality import quality_bp
    from .routes.lineage import lineage_bp
    from .routes.catalog import catalog_bp
    from .routes.openlineage import openlineage_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(datasets_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(quality_bp)
    app.register_blueprint(lineage_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(openlineage_bp)

    return app