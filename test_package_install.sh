#!/bin/bash

if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Deactivating virtual environment..."
    deactivate
fi

if [[ -d "venv" ]]; then
    echo "Removing existing virtual environment..."
    rm -rf venv/
fi

echo "Creating new virtual environment..."
virtualenv venv --python=3.10

echo "Activating virtual environment..."
source venv/scripts/activate

echo "Installing package..."
pip install ./dist/maintainer-0.1.0-py3-none-any.whl

echo "Running app..."
python maintainer/app.py

echo "Success!"
