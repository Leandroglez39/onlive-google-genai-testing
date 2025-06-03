#!/usr/bin/env python3
"""
Main entry point for the Onlive Google GenAI Testing application.

This script provides the main entry point for running the Google Gemini service
with proper module path resolution.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # Now we can import from app
    from app.services.google_gemini import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}")
    print(f"Project root: {project_root}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
