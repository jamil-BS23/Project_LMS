# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (add PostgreSQL client here!)
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements first (better for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make sure wait-for-postgres.sh is executable
RUN chmod +x /app/wait-for-postgres.sh

# Expose FastAPI port
EXPOSE 8000

# Default command (will be overridden by docker-compose entrypoint)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

