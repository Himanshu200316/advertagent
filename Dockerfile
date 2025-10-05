FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for storage
RUN mkdir -p /app/data /app/generated_images

# Install Flask for health checks
RUN pip install Flask==2.3.3

# Create cron job for daily posting
RUN echo "0 0 * * * cd /app && python instagram_agent.py schedule >> /var/log/cron.log 2>&1" | crontab -

# Create log file for cron
RUN touch /var/log/cron.log

# Set permissions
RUN chmod +x /app/instagram_agent.py

# Expose port (if needed for health checks)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Start health check server and cron
CMD ["sh", "-c", "python health_check.py & cron && tail -f /var/log/cron.log"]