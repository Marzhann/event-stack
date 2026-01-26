FROM python:3.12-slim

WORKDIR /app

# System deps (psycopg + build basics)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install deps first (caching)
COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy api code
COPY api /app

# Run
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
 


