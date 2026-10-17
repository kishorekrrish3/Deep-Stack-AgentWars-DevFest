# High-Performance Python 3.11 Slim Image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Copy application code and sample data
COPY logistics_handler ./logistics_handler
COPY data ./data
COPY run_server.py benchmark.py .env.example ./

# Expose API and UI port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Launch uvicorn server
CMD ["python", "run_server.py"]
