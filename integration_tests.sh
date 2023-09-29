#!/bin/bash

# Function to clean up background process
cleanup() {
  kill -9 $API_PID
}

# Register cleanup function to run on script exit
trap cleanup EXIT

# Exit on error
set -e

# Set the API_URL environment variable to the local API server
export API_URL=http://localhost:8000

# Start the API server in the background
uvicorn maintainability.api.src.main:app --port 8000 &
API_PID=$!
sleep 5

# Run the integration tests
pytest
