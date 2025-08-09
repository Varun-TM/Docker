# Docker Todo App

A complete guide to building a Python Flask todo application with Docker, MySQL, and deployment to the cloud.

## Overview

This project demonstrates how to:
- Create a Python Flask app in Docker
- Connect it to MySQL running in another container
- Persist database data using volumes
- Configure environment variables securely
- Use Docker Compose for multi-container setup
- Push your image to Docker Hub
- Scan your image for vulnerabilities
- Deploy it on a cloud server (AWS EC2 or similar)

## Project Structure

```
docker-todo-app/
├── README.md
├── docker-compose.yml
└── app/
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```

## Prerequisites

- Docker and Docker Compose installed
- Docker Hub account
- AWS account (for cloud deployment)
- Basic knowledge of Python, Flask, and Docker

## Step-by-Step Implementation

### Step 1: Project Setup

Create the project structure:

```bash
mkdir docker-todo-app && cd docker-todo-app
mkdir app
```

### Step 2: Create the Flask Application

Create `app/app.py` with a simple todo API that includes:

- **Database configuration** using environment variables for flexible deployment
- **Two API endpoints**:
  - POST `/add` - Accepts JSON data to add new todo tasks
  - GET `/list` - Returns all todo tasks as JSON
- **Database connection management** with proper opening and closing of connections
- **Table creation** on startup to ensure the database schema exists
- **Error handling** for database operations
- **Host binding** to 0.0.0.0 to allow external connections in Docker

### Step 3: Define Python Dependencies

Create `app/requirements.txt` with the necessary Python packages:

- **Flask** - Web framework for creating the API endpoints
- **mysql-connector-python** - Official MySQL driver for Python to connect to the database

### Step 4: Create Dockerfile

Create `app/Dockerfile` with the following configuration:

- **Base image**: Use Python 3.9 slim for a lightweight container
- **Working directory**: Set /app as the working directory inside the container
- **Dependencies installation**: Copy requirements.txt first and install packages for better layer caching
- **Application code**: Copy the application files into the container
- **Port exposure**: Expose port 5000 for the Flask application
- **Startup command**: Define the command to run the Python application

### Step 5: Configure Docker Compose

Create `docker-compose.yml` for multi-container setup with:

**Web Service Configuration:**
- Build the Flask app from the local ./app directory
- Map port 5000 from container to host
- Set environment variables for database connection
- Configure dependency on the database service

**Database Service Configuration:**
- Use official MySQL 8 image
- Set restart policy to always restart on failure
- Configure MySQL root password and database name
- Create a named volume for data persistence

**Volume Definition:**
- Define mysql_data volume for persistent database storage

## Running the Application

### Local Development

1. **Start the application:**
   ```bash
   docker-compose up --build
   ```

2. **Test the API:**
   ```bash
   # Add a todo
   curl -X POST http://localhost:5000/add \
        -H "Content-Type: application/json" \
        -d '{"task": "Learn Docker"}'

   # List todos
   curl http://localhost:5000/list
   ```

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

