# SATQUERY AI — Production Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for geospatial & image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and checkpoints
COPY backend /app/backend
COPY checkpoints /app/checkpoints
COPY data /app/data

# Ensure storage directories exist
RUN mkdir -p /app/storage/uploads /app/storage/generated /app/outputs

ENV PYTHONPATH=/app/backend
ENV PORT=8000
ENV DEMO_MODE=true
ENV MODEL_DEVICE=cpu
ENV FRONTEND_URL=https://frontend-ten-inky-48.vercel.app

EXPOSE 8000

CMD ["sh", "-c", "PYTHONPATH=/app/backend uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
