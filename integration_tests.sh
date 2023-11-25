#!/bin/bash

cleanup() {
  echo "Cleanup function called"
  if [[ -n $API_PID ]]; then
    echo "Killing API process with PID: $API_PID"
    kill -9 $API_PID 2>/dev/null || true
  fi
}

trap cleanup EXIT

# Kill existing process on port 8000
OLD_PID=$(lsof -ti tcp:8000 | head -n 1)
if [[ -n $OLD_PID ]]; then
  echo "Killing old process on port 8000 with PID: $OLD_PID"
  kill -9 $OLD_PID
fi

# Start API
export API_URL=http://localhost:8000
export PYTHONPATH="$PWD"
echo "Starting API..."
poetry run uvicorn maintainability.api.src.main:app --port 8000 &
API_PID=$!
echo "API started with PID: $API_PID"

# Give API time to start
sleep 4

# Run tests
echo "Running tests..."
poetry run pytest -s || exit 1

echo "Tests completed"

# The script will automatically call cleanup upon exit due to the trap command
