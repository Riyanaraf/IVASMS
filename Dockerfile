FROM python:3.11-slim

LABEL maintainer="IVASMS Bot Team"
LABEL description="IVASMS Telegram Bot - SMS Monitoring with Cloudflare Bypass"

WORKDIR /app

# Install system dependencies for Selenium/Chrome support
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    curl \
    chromium-browser \
    chromium-driver \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir python-dotenv

# Copy bot application
COPY bot.py .

# Create non-root user for security
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Health check on built-in health server
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

EXPOSE 10000

# Run bot with error handling
CMD ["python3", "bot.py"]
