from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Job, Run, Dataset, LineageEdge
from datetime import datetime, timezone
import uuid

openlineage_bp = Blueprint("openlineage", __name__)

@openlineage_bp.route("/events", methods=["POST"])
def receive_openlineage_event():
    """
    Consume OpenLineage events and populate the metadata catalog.
    """
    try:
        event = request.get_json()
        if not event:
            return jsonify({"error": "No JSON payload received"}), 400

        # Extract Job info
        job_data = event.get("job", {})
        job_name = job_data.get("name")
        if not job_name:
            return jsonify({"error": "Job name is required"}), 400

        job = Job.query.filter_by(name=job_name).first()
        if not job:
            job = Job()
            job.name = job_name
            db.session.add(job)
            db.session.flush()

        # Extract Run info
        run_data = event.get("run", {})
        run_id_str = run_data.get("runId")
        if not run_id_str:
            return jsonify({"error": "Run ID is required"}), 400
        
        run_id = uuid.UUID(run_id_str)
        run = Run.query.get(run_id)
        
        event_time_str = event.get("eventTime")
        event_time = datetime.fromisoformat(event_time_str.replace("Z", "+00:00")) if event_time_str else datetime.now(timezone.utc)
        
        event_type = event.get("eventType") # START, COMPLETE, FAIL

        if not run:
            run = Run()
            run.id = run_id
            run.job_id = job.id
            run.start_time = event_time
            run.status = event_type
            db.session.add(run)
        else:
            run.status = event_type
            if event_type in ["COMPLETE", "FAIL"]:
                run.end_time = event_time

        # Extract Lineage (Inputs/Outputs)
        inputs = event.get("inputs", [])
        outputs = event.get("outputs", [])

        for inp in inputs:
            ds_name = inp.get("name")
            ds_uri = inp.get("namespace") + "/" + ds_name if inp.get("namespace") else ds_name
            dataset = Dataset.query.filter_by(uri=ds_uri).first()
            if not dataset:
                dataset = Dataset()
                dataset.name = ds_name
                dataset.uri = ds_uri
                db.session.add(dataset)
                db.session.flush()

            # Create lineage edges for outputs
            for out in outputs:
                out_name = out.get("name")
                out_uri = out.get("namespace") + "/" + out_name if out.get("namespace") else out_name
                out_dataset = Dataset.query.filter_by(uri=out_uri).first()
                if not out_dataset:
                    out_dataset = Dataset()
                    out_dataset.name = out_name
                    out_dataset.uri = out_uri
                    db.session.add(out_dataset)
                    db.session.flush()

                # Add edge: Input -> Output
                edge = LineageEdge.query.filter_by(
                    source_dataset_id=dataset.id,
                    target_dataset_id=out_dataset.id,
                    job_run_id=run.id
                ).first()
                if not edge:
                    edge = LineageEdge()
                    edge.source_dataset_id = dataset.id
                    edge.target_dataset_id = out_dataset.id
                    edge.job_run_id = run.id
                    edge.edge_type = "INPUT_TO_OUTPUT"
                    db.session.add(edge)

        db.session.commit()
        return jsonify({"status": "event processed", "run_id": str(run.id)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
