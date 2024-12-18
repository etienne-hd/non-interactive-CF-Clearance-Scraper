# Use a slim version of Python 3.9 as the base image
FROM python:3.9-slim

# Update apt package list and install necessary libraries for Chromium and Playwright
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libdrm2 \
    libxcb1 \
    libxkbcommon0 \
    libasound2 \
    libxfixes3 \
    && rm -rf /var/lib/apt/lists/*  # Clean up package lists to reduce image size

# Set environment variables for server configuration
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=5000
ENV SERVER_WORKER=5
ENV DEBUG=FALSE

# Set the working directory to /app
WORKDIR /app

# Copy the current directory's contents into the /app directory in the container
COPY . /app

# Install the required Python packages from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Install Chromium for Playwright
RUN python -m playwright install chromium

# Expose the server port to allow access from outside the container
EXPOSE $SERVER_PORT

# Run the application using Gunicorn with specified number of workers
CMD ["sh", "-c", "gunicorn -b $SERVER_HOST:$SERVER_PORT --workers $SERVER_WORKER server:app"]
