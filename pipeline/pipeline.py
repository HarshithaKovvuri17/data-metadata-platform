import pandas as pd
import requests
import uuid
import os
from datetime import datetime
from dataclasses import asdict

# OpenLineage
from openlineage.client import OpenLineageClient, set_producer
from openlineage.client.run import Job, Run, RunEvent, RunState, Dataset as OLDataset
from openlineage.client.facet import SchemaDatasetFacet, SchemaField

# Soda Import - This will now work after installing soda-core-scientific
try:
    import importlib
    soda_scan = importlib.import_module("soda.scan")
    Scan = getattr(soda_scan, "Scan")
except Exception:
    print("CRITICAL: soda-core-scientific not found. Run: pip install soda-core-scientific")
    Scan = None

# Configuration
API_URL = os.getenv("METADATA_API_URL", "http://api:5000")
DATA_PATH = "/app/data/sample_products.csv"
JOB_NAME = "product_ingestion_pipeline"
NAMESPACE = "food_platform"
PRODUCER = "https://github.com/my-org/metadata-pipeline"

client = OpenLineageClient(url=API_URL, options=None)
set_producer(PRODUCER)

def run_pipeline():
    if Scan is None: return

    run_id = str(uuid.uuid4())
    ol_job = Job(namespace=NAMESPACE, name=JOB_NAME)
    ol_run = Run(runId=run_id)
    
    # 1. Start Lineage
    try:
        start_event = RunEvent(
            eventType=RunState.START,
            eventTime=datetime.utcnow().isoformat() + "Z",
            run=ol_run,
            job=ol_job,
            producer=PRODUCER,
            inputs=[],
            outputs=[]
        )
        requests.post(f"{API_URL}/openlineage/events", json=asdict(start_event))
    except Exception: pass

    try:
        # 2. Ingest
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)
        else:
            df = pd.DataFrame({'id': [1, 2], 'price': [10.0, 15.0]})

        # 3. Soda Quality Scan (Updated for v4.x)
        scan = Scan()
        scan.set_scan_definition_name("product_quality_run")
        
        # In v4, we must explicitly define a pandas data source
        scan.add_pandas_dataframe(
            dataset_name="sample_products", 
            df=df, 
            data_source_name="my_pandas_source"
        )
        
        checks_yaml = """
        checks for sample_products:
          - row_count > 0
          - missing_count(id) = 0
          - min(price) > 0
        """
        scan.add_sodacl_yaml_str(checks_yaml)
        
        print("Executing Soda Scan...")
        scan.execute()
        
        # 4. Extract Results
        dq_results = []
        for check in scan._checks:
            dq_results.append({
                "check_name": check.name,
                "success": check.outcome == "pass",
                "observed_value": str(check.check_value)
            })

        requests.post(f"{API_URL}/runs/{run_id}/dq_results", json={
            "dataset_uri": f"{NAMESPACE}/sample_products",
            "results": dq_results
        })

        # 5. Complete Lineage
        schema = [{"name": col, "type": str(dtype)} for col, dtype in df.dtypes.items()]
        fields = [SchemaField(name=c['name'], type=c['type']) for c in schema]
        output_ds = OLDataset(namespace=NAMESPACE, name="sample_products", facets={"schema": SchemaDatasetFacet(fields=fields)})

        complete_event = RunEvent(
            eventType=RunState.COMPLETE,
            eventTime=datetime.utcnow().isoformat() + "Z",
            run=ol_run,
            job=ol_job,
            producer=PRODUCER,
            inputs=[],
            outputs=[output_ds]
        )
        requests.post(f"{API_URL}/openlineage/events", json=asdict(complete_event))
        print(f"Pipeline finished. Run ID: {run_id}")

    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run_pipeline()