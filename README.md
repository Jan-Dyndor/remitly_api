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

## Running the Remitly API Application with Docker

This document outlines the necessary steps to download, build, and run the Remitly API application using Docker and Docker Compose.

### Requirements

Before you begin, ensure you have the following tools installed on your machine:

* **Docker:** [Download and install Docker](https://www.docker.com/get-started)
* **Docker Compose:** Typically installed with Docker Desktop. If you only have Docker Engine, you might need to install it separately. Refer to the Docker documentation.

### Getting Started

1.  **Download the Repository from GitHub:**

    Open your terminal or command prompt and navigate to the directory where you want to clone the repository. Then, execute the following command:

    ```bash
    git clone [https://github.com/Jan-Dyndor/remitly_api.git](https://github.com/Jan-Dyndor/remitly_api.git)
    cd remitly_api
    ```

    Replace `https://github.com/Jan-Dyndor/remitly_api.git` with the actual URL of your repository.

2.  **Run the Application with Docker Compose:**

    In the root directory of the downloaded repository (where the `docker-compose.yml` file is located), execute the command:

    ```bash
    docker-compose up --build
    ```

    * `docker-compose up`: This command creates and starts the containers defined in your `docker-compose.yml` file.
    * `--build`: This flag ensures that Docker Compose first builds the Docker image based on your `Dockerfile` if the image doesn't exist or has changed.

    Wait for Docker to download the necessary base images, build your application image, and start the container. In the logs, you should see information about the database creation and the Uvicorn server starting on port `8080`.

3.  **Access the Application:**

    Once the container has started successfully, your API application will be accessible at `http://localhost:8080` in your web browser or using a tool like `curl`.

    * **API Documentation (Swagger UI):** Available at `http://localhost:8080/docs`.
    * **OpenAPI Schema:** Available at `http://localhost:8080/openapi.json`.

### Additional Docker Compose Commands

* **Run in Detached Mode (Background):**

    ```bash
    docker-compose up -d
    ```

    This command starts the containers in the background and frees up your terminal.

* **View Container Logs:**

    ```bash
    docker-compose logs web
    ```

    Replace `web` with the name of your application service (as defined in `docker-compose.yml`).

* **Stop and Remove Containers:**

    ```bash
    docker-compose down
    ```

    This command stops and removes the containers and the network created by `docker-compose up`.

### Troubleshooting

* **`FileNotFoundError` for CSV File:** If you encounter an error related to a missing CSV file (`interns_2025_swift_codes.csv`), ensure that this file is located in the `data/` directory within your local repository **before** running `docker-compose up --build`. Also, check your `.dockerignore` file to ensure it's not excluding the `data/` directory or `.csv` files.

* **Port Conflicts:** If port `8080` is already in use on your machine, change the port mapping in the `ports` section of your `docker-compose.yml` file (e.g., to `8000:8080`).

* **Build Errors:** Analyze the Docker build logs for any errors in your `Dockerfile` or during dependency installation.

