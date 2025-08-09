# Multi-stage Dockerfile for production optimization

# Development stage
FROM python:3.9-slim as development

WORKDIR /app

# Install development dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Development configuration
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000
CMD ["python", "app.py"]

# Production stage
FROM python:3.9-slim as production

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install only production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip/*

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Production configuration
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

EXPOSE 5000
CMD ["python", "app.py"]
