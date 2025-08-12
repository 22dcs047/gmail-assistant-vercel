# Simple run script for Gmail Assistant - Fixed
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced app
try:
    from api.app import app, gmail_assistant
    
    # Add missing openai_client attribute for compatibility
    if not hasattr(gmail_assistant, 'openai_client'):
        gmail_assistant.openai_client = None
    
    print("🚀 Starting Enhanced Gmail Assistant...")
    print(f"📧 Gmail Connected: {bool(gmail_assistant.gmail_service)}")
    print(f"🧠 OpenAI Connected: {bool(getattr(gmail_assistant, 'openai_client', None))}")
    print("🌐 Visit: http://localhost:5000")
    print("🔍 Debug: http://localhost:5000/debug")
    
    app.run(debug=True, port=5000)
    
except Exception as e:
    print(f"❌ Error starting app: {e}")
    print("Please check your setup and try again.")
