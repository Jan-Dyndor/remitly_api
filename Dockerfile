
FROM python:3.12-slim


WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .



ENV PYTHONPATH=/app

# new data baase every time container runs
CMD ["bash", "-c", "python app/init_db.py && python app/export_data_to_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8080"]

