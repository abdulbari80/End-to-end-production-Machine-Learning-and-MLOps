# Use slim Python base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy dependencies first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copy project files
COPY . .

# Expose port 8000 (Azure expects the container to listen here)
EXPOSE 8000

# Use gunicorn as a production server
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
