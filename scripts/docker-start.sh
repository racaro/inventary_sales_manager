#!/bin/bash

set -e  # Exit on any error

echo "Stock Manager Docker Startup Script"
echo "===================================="

# Check if Docker is running
echo "Checking if Docker is running..."
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running."
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "Docker is running"

# Stop any existing containers
echo "Stopping any existing containers..."
docker-compose down 2>/dev/null || true

# Build the Docker image
echo "Building Stock Manager Docker image..."
if ! docker-compose build; then
    echo "Error building Docker image."
    echo "Please check the logs above for details."
    exit 1
fi

echo "Docker image built successfully"

# Start the container
echo "Starting Stock Manager container..."
if ! docker-compose up -d; then
    echo "Error starting container."
    echo "Please check the logs above for details."
    exit 1
fi

echo "Stock Manager container started successfully"
echo "Waiting for services to start..."
sleep 3

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo "All services are running!"
    echo "Ready to connect via VNC to localhost:5901"
else
    echo "Container may not be fully ready yet. Check logs with:"
    echo "   docker-compose logs -f stock-manager"
fi

echo ""
echo "Press any key to continue..."
read -n 1 -s
