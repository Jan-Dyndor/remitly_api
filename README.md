# Remitly SWIFT API

A RESTful API application for accessing and managing SWIFT/BIC code data. Built with FastAPI, SQLAlchemy and SQLite, and containerized using Docker.

---

## 🔧 Features

- Parse and store SWIFT code data from CSV
- Headquarters and branch identification
- Retrieve SWIFT data by code or country
- Add and delete SWIFT entries
- Input validation and proper error handling
- Unit and integration tests
- Dockerized for easy deployment

## 🚀 Setup Instructions

### 1. Clone the repository

Go to:
...cd remitly_api
Install
python -m venv venv
set $env:PYTHONPATH="."  
 .\venv\Scripts\Activate
pip install -r requirements.txt

Build and run Docker
docker build -t remitly-api .
docker run -p 8080:8080 remitly-api

FastAPI Swagger docs will be available at:
http://localhost:8080/docs

Load Database
python app/init_db.py

Load CSV
jupyter notebook app/explore_data_export_to_db.ipynb

Run tests
pytest app/tests
