#!/usr/bin/env bash
# start.sh — Run FastAPI app on Render

set -o errexit
set -o pipefail
set -o nounset

echo "Running Alembic migrations..."
if alembic upgrade head; then
    echo "Migrations applied successfully."
else
    echo "No migrations found or Alembic not configured."
fi

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
