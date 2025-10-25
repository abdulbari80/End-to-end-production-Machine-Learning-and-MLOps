# Use Python 3.12 slim image
FROM python:3.12.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt setup.py ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .
COPY artifacts/ ./artifacts/

# Expose port
EXPOSE 80

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app", "--workers", "1", "--timeout", "120"]

