# Web Development 50-Minute Challenge

This repository contains a full-stack web application developed to meet the requirements of the 5-step web development challenge, including a static frontend, an external API integration, a REST backend, Git versioning, and Cloud-ready Docker containerization.

## Project Structure

* `frontend/`: Contains the HTML, CSS, and JavaScript files.
* `backend/`: Contains the FastAPI application and SQLite database.

## How to Run (Docker - Recommended)

The easiest way to run the application is using Docker Compose. This ensures the environment is identical to the production cloud environment.

1. Ensure `docker` and `docker-compose` (or `docker compose` plugin) are installed.
2. Navigate to the root directory of the project.
3. Run the following command:
   ```bash
   docker compose up --build
    ```
## How to Run (Bash)

1. Navigate to root and run:
    ```bash
    ./run.sh
    ```
