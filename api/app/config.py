import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://metadata_user:metadata_pass@metadata_postgres:5432/metadata_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
