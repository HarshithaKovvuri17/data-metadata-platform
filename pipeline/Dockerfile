FROM python:3.11-slim

WORKDIR /pipeline

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

CMD ["python", "pipeline.py"]