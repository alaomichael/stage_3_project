# Flask-Celery Email Task

## Project Overview

This project demonstrates a simple Flask application integrated with Celery to handle background tasks. The main task is sending emails using Flask-Mail.

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Environment Variables

Create a `.env` file in the project root and add the following variables:


### Installation

1. Clone the repository:
    ```
    git clone https://github.com/alaomichael/stage_3_project.git
    cd stage_3_project
    ```

2. Build the Docker image for Celery:
    ```
    docker build -t celery-app -f Dockerfile.celery .
    ```

3. Run the Redis container:
    ```
    docker run -d -p 6379:6379 redis
    ```

## Running the Flask App

1. Run the Flask app:
    ```
    python app.py
    ```

## Running the Celery Worker

1. Run the Celery worker:
    ```
    docker run --env-file .env -v $(pwd):/app celery-app
    ```

## Using the Application

- Navigate to `http://localhost:5000` to access the Flask app.
- Use `http://localhost:5000/?sendmail=recipient@example.com` to send an email.
- Use `http://localhost:5000/?talktome=1` to log a message.
- Check logs at `http://localhost:5000/logs`.

