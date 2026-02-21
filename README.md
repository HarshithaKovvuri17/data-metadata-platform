
# 📊 Mini Data Governance Platform
### Metadata Catalog • Data Quality Monitoring • Data Lineage Tracking

---

## 🧠 Overview
Modern organizations must understand, trust, and trace their data.

This project builds a mini data platform implementing:

- 📚 Metadata Catalog
- 🧪 Data Quality Monitoring
- 🔗 Data Lineage Tracking

The system acts as a **central source of truth** for datasets.

---

## 🎯 Objective
This platform demonstrates how real data platforms (DataHub/OpenMetadata) work internally.

We built:

✔ Flask metadata catalog API  
✔ PostgreSQL metadata database  
✔ Python data pipeline  
✔ Great Expectations data quality checks  
✔ OpenLineage lineage tracking  
✔ Dockerized reproducible environment  

---

## 🏗️ Architecture

CSV Dataset
      ↓
Python Data Pipeline
  - schema extraction
  - statistics
  - data quality checks
  - lineage events
      ↓
Flask Metadata API
      ↓
PostgreSQL Database

---

## 📂 Project Structure

data-metadata-platform/
│
├
├── api/                      ← Flask Metadata Catalog
│     ├── app/
│     │   ├── __init__.py
│     │   ├── models.py
│     │   ├── schemas.py
│     │   ├── routes/
│     │   │   ├── datasets.py
│     │   │   ├── lineage.py
│     │   │   ├── search.py
│     │   │   └── openlineage.py
│     │   ├── services/
│     │   │   ├── dataset_service.py
│     │   │   ├── lineage_service.py
│     │   │   └── dq_service.py
│     │   ├── config.py
│     │   └── extensions.py
│     │
│     ├── run.py
│     ├── wait_for_db.py
│     ├── requirements.txt
│     └── Dockerfile
│   
│── pipeline/                 ← Data Processing Worker
│       ├── pipeline.py
│       ├── dq_checks.py
│       ├── metadata_client.py
│       ├── lineage_emitter.py
│       ├── requirements.txt
│       └── Dockerfile
│
├── database/
│   └── init.sql                  ← DB schema creation
│
├── data/
│   └── sample_products.csv       ← dataset used in pipeline
│
├── examples/                     ← required by evaluation
│   ├── openlineage_start.json
│   └── openlineage_complete.json
│
├── tests/                        ← automated validation
│   └── test_api.py
│
├── docker-compose.yml
├── submission.yml
├── data_quality_report.md
├── README.md
└── generate_readme.py

---

## 🗄️ Database Tables

| Table | Purpose |
|------|------|
| datasets | dataset metadata |
| columns | schema |
| column_statistics | null %, distinct count |
| jobs | pipeline jobs |
| runs | job executions |
| data_quality_results | DQ outcomes |
| lineage_edges | lineage graph |

---

## 🚀 Setup

### Start platform
docker compose up --build

### Run pipeline
docker compose run pipeline python pipeline/pipeline.py

---

## 🔌 API Endpoints

POST /datasets → register dataset  
GET /datasets/{id} → metadata profile  
GET /datasets/{id}/lineage → lineage graph  
GET /search?q= → dataset search  
POST /openlineage/events → lineage ingestion

---

## 🧪 Data Quality Checks

Using Great Expectations:

- not null validation
- unique validation
- allowed values
- numeric ranges
- positive values

Results stored in metadata catalog.

---

## 🔗 Lineage

Pipeline emits:

START → COMPLETE → FAIL

Graph stored as:

Input Dataset → Job → Output Dataset

---

## 🐳 Docker Services

| Service | Port |
|------|------|
| API | 5000 |
| PostgreSQL | 5432 |

Run everything:

docker compose up

---

## 🧪 Automated Evaluation

Setup:
docker compose up -d --build

Run:
docker compose run pipeline python pipeline/pipeline.py

Test:
API validation queries verify metadata persistence.

---

## 🧩 Technologies

Flask  
PostgreSQL  
SQLAlchemy  
Great Expectations  
OpenLineage  
Docker  
Pandas

---

## ⭐ Features

✔ Metadata discovery  
✔ Dataset search  
✔ Column statistics  
✔ Data quality monitoring  
✔ Lineage tracking  
✔ REST APIs  
✔ Fully dockerized

---

## 🧑‍💻 Author
Harshitha Kovvuri

---
