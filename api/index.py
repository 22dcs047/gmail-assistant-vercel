# Vercel entry point
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("✅ Successfully imported app")
except Exception as e:
    print(f"❌ Import failed: {e}")
    # Simple fallback
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def fallback():
        return '''
        <h1>🚀 Gmail Assistant</h1>
        <p>Service is loading...</p>
        <p style="color: red;">Import issue detected. Please check logs.</p>
        '''

# Export for Vercel
if __name__ == "__main__":
    app.run()
