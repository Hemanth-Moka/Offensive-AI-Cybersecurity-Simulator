# Multi-stage Docker build for Offensive AI Platform

# ================================================
# STAGE 1: Backend Builder
# ================================================

FROM python:3.11-slim as backend-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ================================================
# STAGE 2: Production Backend
# ================================================

FROM python:3.11-slim as backend-prod

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy application code
COPY backend/ .

# Create non-root user
RUN useradd -m -u 1000 appuser
RUN chown -R appuser:appuser /app
USER appuser

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')" || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ================================================
# STAGE 3: Frontend Builder
# ================================================

FROM node:20-alpine as frontend-builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Build
RUN npm run build

# ================================================
# STAGE 4: Production Frontend
# ================================================

FROM node:20-alpine as frontend-prod

WORKDIR /app

RUN npm install -g serve

# Copy built application from builder
COPY --from=frontend-builder /app/dist ./dist

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Run
CMD ["serve", "-s", "dist", "-l", "3000"]

# ================================================
# FINAL STAGE: Development/Production selector
# ================================================

FROM backend-prod as production

LABEL maintainer="Offensive AI Team"
LABEL version="1.0.0"
LABEL description="Offensive AI - Cybersecurity Awareness Platform"
