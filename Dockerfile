# Official lightweight base image with SQLite
FROM python:3.9-slim

# Install SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /opt/sqlcoder_env

# Set environment variables
ENV PATH="/opt/sqlcoder_env/bin:$PATH"
ENV PYTHONPATH=/app

# Copy the SQL script into the container
COPY scripts/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir hf_xet

# Copy app and sceipts directories
COPY app/ .
COPY scripts/ /scripts/

# Ensure entrypoint script executable
RUN chmod +x /scripts/entrypoint.sh

# Expose FastAPI port
EXPOSE 8080

# Run the SQL script to create and populate the databse
ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]