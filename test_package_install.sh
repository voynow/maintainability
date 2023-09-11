#!/bin/bash

set -e  # Stop on first error

if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Deactivating virtual environment..."
    deactivate
fi

if [[ -d "dist" ]]; then
    echo "Removing existing dist directory..."
    rm -rf dist/
fi

if [[ -d "venv" ]]; then
    echo "Removing existing virtual environment..."
    rm -rf venv/
fi

echo "Creating new virtual environment..."
virtualenv venv --python=3.10

echo "Activating virtual environment..."
source venv/scripts/activate

echo "Building package..."
poetry build

echo "Installing package..."
pip install ./dist/maintainability-0.1.0-py3-none-any.whl

echo "Running app..."
python maintainability/app.py

echo "Success!"
