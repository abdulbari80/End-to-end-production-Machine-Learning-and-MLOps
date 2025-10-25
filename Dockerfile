# Use Python 3.12 slim
FROM python:3.12.11-slim

# Set working directory
WORKDIR /app

# Copy only the files needed for dependencies
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Flask default)
EXPOSE 80

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
