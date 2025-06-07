# Use a base Python image
FROM python:3.9-slim

# Install system dependencies required for dlib and face_recognition
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
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Railway will use
EXPOSE 5000

# Use environment variable PORT or default to 5000
ENV PORT=5000

# Start the Flask app (modify if your main file isn't app.py)
CMD ["python", "app.py"]
