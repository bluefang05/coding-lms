# Pandas Gamified LMS - Docker Image
# Multi-stage build for production deployment

FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    sqlite3 \
    libsqlite3-dev \
    php \
    php-sqlite3 \
    php-mbstring \
    php-xml \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/datasets notebooks uploads exports && \
    chmod -R 755 data notebooks uploads exports

# Initialize database and generate datasets
RUN python backend/init_database.py && \
    python backend/sample_datasets/generate_datasets.py

# Expose ports
EXPOSE 8888 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

# Default command
CMD ["sh", "-c", "php -S 0.0.0.0:80 & jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root"]

# Development image with additional tools
FROM base as development

RUN pip install \
    pytest-cov \
    black \
    flake8 \
    mypy \
    jupyterlab

EXPOSE 8889

CMD ["sh", "-c", "php -S 0.0.0.0:80 & jupyter lab --ip=0.0.0.0 --port=8889 --no-browser --allow-root"]
