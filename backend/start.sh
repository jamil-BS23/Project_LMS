#!/usr/bin/env bash
# start.sh — Run FastAPI app on Render

# Exit immediately if a command exits with a non-zero status.
set -o errexit
set -o pipefail
set -o nounset

# Ensure greenlet is available (important for SQLAlchemy async)
echo "Installing stable greenlet version..."
pip install --no-cache-dir greenlet==3.0.3

# Run Alembic migrations if using Alembic
echo "Running Alembic migrations..."
if alembic upgrade head; then
    echo "Migrations applied successfully."
else
    echo "No migrations found or Alembic not configured."
fi

# Start the FastAPI app using Uvicorn
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
