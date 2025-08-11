# Vercel Python Runtime Entry Point
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# This is the entry point for Vercel
handler = app

# For local testing
if __name__ == "__main__":
    app.run()
