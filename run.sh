#!/bin/bash
"""
Run script for the Onlive Google GenAI Testing application.

This script ensures the proper environment is activated and runs the application
with the correct Python path configuration.
"""

# Change to the directory containing this script
cd "$(dirname "$0")"

# Check if we're in a Poetry environment
if command -v poetry &> /dev/null; then
    echo "Running with Poetry..."
    poetry run python -m app.services.google_gemini
else
    # Fallback to direct Python execution
    echo "Running with direct Python execution..."
    python main.py
fi
