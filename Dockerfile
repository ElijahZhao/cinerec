# CineRec — Multi-Modal Movie Recommendation System
# Multi-stage Docker build

# Stage 1: Python dependencies
FROM python:3.10-slim AS deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy Python packages from deps stage
COPY --from=deps /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/movies?page=1\&per_page=1 || exit 1

# Start command
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
