# Base image with Python & build tools
FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install OS dependencies required for dlib & face_recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    python3-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optional: for timezone issues
ENV TZ=Asia/Kolkata

# Create app directory
WORKDIR /app

# Copy requirements.txt first to cache dependencies
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY . .

# Port to expose
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]


face_recognition
flask
flask-cors
