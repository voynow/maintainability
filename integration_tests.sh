#!/bin/bash

cleanup() {
  if [[ -n $API_PID ]]; then
    taskkill //PID $API_PID //F 2>/dev/null || true
  fi
}

trap cleanup EXIT

# Kill existing process on port 8000
OLD_PID=$(netstat -ano | findstr :8000 | awk '{print $5}' | head -n 1)
if [[ -n $OLD_PID ]]; then
  taskkill //PID $OLD_PID //F
fi

# Start API
export API_URL=http://localhost:8000
export PYTHONPATH="$PWD"
poetry run uvicorn maintainability.api.main:app --port 8000 &
API_PID=$!

# Give API time to start
sleep 4

# Run tests
poetry run pytest || exit 1