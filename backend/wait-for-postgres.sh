#!/bin/bash
set -e

echo "Waiting for Postgres..."

# Wait until Postgres is ready
until pg_isready -h postgres -p 5432 -U postgres; do
  sleep 1
done

echo "Postgres is ready, starting backend..."
exec "$@"
