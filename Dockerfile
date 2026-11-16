FROM python:3.11-slim

WORKDIR /app

# Install build essentials if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (including pre-compiled frontend/dist)
COPY . .

# Expose default port
EXPOSE 8000

# Command to run unified FastAPI + React server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
