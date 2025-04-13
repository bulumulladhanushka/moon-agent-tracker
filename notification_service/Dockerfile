# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (optional but good for packages like pymysql)
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the port Flask is running on
EXPOSE 5003

# Run the application
CMD ["python", "app.py"]

