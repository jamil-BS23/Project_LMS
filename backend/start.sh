#!/usr/bin/env bash
# start.sh — Run FastAPI app on Render

# Exit immediately if a command exits with a non-zero status.
set -o errexit

# Run database migrations if using Alembic
echo "Running Alembic migrations..."
alembic upgrade head || echo "No migrations found or Alembic not configured."

# Start the FastAPI app using Uvicorn
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
