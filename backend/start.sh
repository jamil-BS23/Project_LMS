#!/usr/bin/env bash
set -e

# Wait for DB to be ready (small loop)
# (optional) replace with more robust wait-for if you want
for i in {1..20}; do
  if python - <<'PY'
import sys, urllib.parse, os, asyncpg, asyncio
from sqlalchemy.engine.url import make_url
url = os.environ.get("DATABASE_URL")
if not url:
    sys.exit(1)
# Convert psycopg if necessary, but asyncpg expects asyncpg style; alembic uses sync engine.
# We keep this small: just attempt a sync tcp connect via asyncpg.
async def try_connect():
    try:
        u = make_url(url)
        host = u.host or "localhost"
        port = u.port or 5432
        await asyncpg.connect(f'postgresql://{u.username}:{u.password}@{host}:{port}/{u.database}')
        print("DB OK")
        sys.exit(0)
    except Exception as e:
        # print(e)
        sys.exit(2)
asyncio.run(try_connect())
PY
  then
    echo "DB up"
    break
  else
    echo "Waiting for DB... ($i/20)"
    sleep 2
  fi
done

# Run Alembic migrations
cd "$(dirname "$0")"
# If alembic is configured with env variable DATABASE_URL this will run.
alembic upgrade head

# Start the app using $PORT provided by Render
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-10000}"
