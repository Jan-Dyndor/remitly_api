# Remitly SWIFT API

A RESTful API application for accessing and managing SWIFT code data. Built with FastAPI, SQLAlchemy and SQLite, and containerized using Docker.

---

## 🔧 Features

- Parses SWIFT code data from a provided `.csv` file.
- Stores data in an SQLite database using SQLAlchemy.
- Normalizes and capitalizes all country codes and names.
- Identifies headquarter vs branch based on the SWIFT code suffix.
- Offers fully RESTful API endpoints with Swagger UI documentation.
- Provides unit and integration tests.
- Fully containerized with **Docker + Docker Compose**.
- Deploys API on `localhost:8080`.

## ⚙️ How It Works

- All SWIFT codes ending in `XXX` are treated as **headquarters**.
- If the SWIFT code has the same first 8 characters as a headquarter, it’s considered a **branch**.
- Country names and ISO2 codes are normalized to uppercase before saving.
- The data is parsed from a provided CSV and saved into an SQLite database when the container starts.

## 🚀 Setup Instructions

## Running the Remitly API Application with Docker

This document outlines the necessary steps to download, build, and run the Remitly API application using Docker and Docker Compose.

### Requirements

Before you begin, ensure you have the following tools installed on your machine:

- ⚠️ **CSV file** ⚠️ The required CSV file is not stored in the repository for security and compliance reasons. It should be created from the spreadsheet given to interns as data in order to create API

1. Download the original Excel file named:
   `Interns_2025_SWIFT_CODES` (provided as part of the recruitment assignment)
2. Open it and **save it as CSV**
3. Rename the file to (if needed): `Interns_2025_SWIFT_CODES - Sheet1.csv`
4. Place the file in the following directory:
   ```bash
   remitly_api/app/data/
   ```

- **Docker:**
- **Docker Compose:** Typically installed with Docker Desktop. If you only have Docker Engine, you might need to install it separately. Refer to the Docker documentation.

## 🧾 API Endpoints Overview

### ✅ `GET /v1/swift-codes/{swiftCode}`

- Returns a **single SWIFT code** entry.
- If it’s a **headquarter**, also returns a list of branches matching first 8 chars of the code.
- Returns 404 if not found.

### ✅ `GET /v1/swift-codes/country/{countryISO2}`

- Returns **all SWIFT codes** for a given country (2-letter ISO code).
- Normalizes lower/upper case input.

### ✅ `POST /v1/swift-codes`

- Adds a new SWIFT code.
- Returns 201 on success or 409 if the code already exists.

### ✅ `DELETE /v1/swift-codes/{swiftCode}`

- Deletes a SWIFT code if it exists.
- Returns 200 on success or 404 otherwise.

# Getting Started

1.  **Download the Repository from GitHub:**

    Open your terminal or command prompt and navigate to the directory where you want to clone the repository. Then, execute the following command:

    ```bash
    git clone https://github.com/Jan-Dyndor/remitly_api.git
    cd remitly_api
    ```

2.  **The app does not include the .csv file in the repository.**
    You must manually add the CSV file before starting the app.
    In order to do so, convert excel spreadsheet to CSV format and place it in **data** folder.

    ```bash
    remitly_api/app/data/
    ```

    Make sure it is named exactly:

    ```bash
     Interns_2025_SWIFT_CODES - Sheet1.csv
    ```

    This repository excludes cache and sensitive files using .gitignore and .dockerignore. The SQLite database is recreated and loaded from the CSV each time you rebuild the Docker image.

3.  **Run the Application with Docker Compose:**

    In the root directory of the downloaded repository (where the `docker-compose.yml` file is located), execute the command:

    ```bash
    docker-compose up --build
    ```

    - `docker-compose up`: This command creates and starts the containers defined in your `docker-compose.yml` file.
    - `--build`: This flag ensures that Docker Compose first builds the Docker image based on your `Dockerfile` if the image doesn't exist or has changed.

    Wait for Docker to download the necessary base images, build your application image, and start the container. In the logs, you should see information about the database creation and the Uvicorn server starting on port `8080`.

    If image is already created use `docker-compose up`.

4.  **Access the Application:**

    Once the container has started successfully, your API application will be accessible at `http://localhost:8080` in your web browser or using a tool like `curl`.

    - **API Documentation (Swagger UI):** Available at `http://localhost:8080/docs`.
    - **OpenAPI schema** Available at `http://localhost:8080/openapi.json`.

5.  **TESTING**
    After running the container with:

    ```bash
    docker compose up --build
    ```

    or

    ```bash
    docker compose up
    ```

    In **another** terminal run:

    ```bash
    docker exec -it remitly_api-web-1 pytest
    ```

    Tests are stred in tests folder, can be runed locally

### Troubleshooting

- **`FileNotFoundError` for CSV File:** If you encounter an error related to a missing CSV file (`Interns_2025_SWIFT_CODES - Sheet1.csv`), ensure that this file is located in the `data/` directory within your local repository **before** running `docker-compose up --build`. Also, check your `.dockerignore` file to ensure it's not excluding the `data/` directory or `.csv` files.

- **Port Conflicts:** If port `8080` is already in use on your machine, change the port mapping in the `ports` section of your `docker-compose.yml` file (e.g., to `8000:8080`).

- **Build Errors:** Analyze the Docker build logs for any errors in your `Dockerfile` or during dependency installation.
