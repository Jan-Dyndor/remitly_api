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

## Running the Remitly API Application with Docker

This document outlines the necessary steps to download, build, and run the Remitly API application using Docker and Docker Compose.

### Requirements

Before you begin, ensure you have the following tools installed on your machine:

- **Docker:**
- **Docker Compose:** Typically installed with Docker Desktop. If you only have Docker Engine, you might need to install it separately. Refer to the Docker documentation.
- **CSV file** of a spreadsheet given to interns as data in order to create API

### Getting Started

1.  **Download the Repository from GitHub:**

    Open your terminal or command prompt and navigate to the directory where you want to clone the repository. Then, execute the following command:

    ```bash
    git clone https://github.com/Jan-Dyndor/remitly_api.git
    cd remitly_api
    ```

2.  **The app does not include the .csv file in the repository (to avoid large data files in version control).**
    You must manually add the CSV file before starting the app.
    In order to do so, convert exel spreadsheet to CSV format and place it in data folder. Consider naming confention as follows: `Interns_2025_SWIFT_CODES - Sheet1.csv`
    remitly_api/
    └── app/
    └── data/
    └── Interns_2025_SWIFT_CODES - Sheet1.csv

    If you are interesetd in data exploration, you need to add the file path to explore_data.ipynb file

3.  **Run the Application with Docker Compose:**

    In the root directory of the downloaded repository (where the `docker-compose.yml` file is located), execute the command:

    ```bash
    docker-compose up --build
    ```

    - `docker-compose up`: This command creates and starts the containers defined in your `docker-compose.yml` file.
    - `--build`: This flag ensures that Docker Compose first builds the Docker image based on your `Dockerfile` if the image doesn't exist or has changed.

    Wait for Docker to download the necessary base images, build your application image, and start the container. In the logs, you should see information about the database creation and the Uvicorn server starting on port `8080`.

4.  **Access the Application:**

    Once the container has started successfully, your API application will be accessible at `http://localhost:8080` in your web browser or using a tool like `curl`.

    - **API Documentation (Swagger UI):** Available at `http://localhost:8080/docs`.
    - **OpenAPI schema** Available at `http://localhost:8080/openapi.json`.

### Troubleshooting

- **`FileNotFoundError` for CSV File:** If you encounter an error related to a missing CSV file (`Interns_2025_SWIFT_CODES - Sheet1.csv`), ensure that this file is located in the `data/` directory within your local repository **before** running `docker-compose up --build`. Also, check your `.dockerignore` file to ensure it's not excluding the `data/` directory or `.csv` files.

- **Port Conflicts:** If port `8080` is already in use on your machine, change the port mapping in the `ports` section of your `docker-compose.yml` file (e.g., to `8000:8080`).

- **Build Errors:** Analyze the Docker build logs for any errors in your `Dockerfile` or during dependency installation.
