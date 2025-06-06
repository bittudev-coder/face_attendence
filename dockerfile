# Base image with Python
FROM python:3.9-slim

# Install system dependencies required by dlib and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk-3-dev \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libffi-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application files
COPY . .

# Expose port (if needed)
EXPOSE 5000

# Run your app
CMD ["python", "app.py"]
