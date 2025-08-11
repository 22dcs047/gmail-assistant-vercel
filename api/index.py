# Vercel Python Runtime Entry Point
from flask import Flask
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main app
try:
    from app import app
    print("✅ Successfully imported app")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    # Create a minimal Flask app as fallback
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return """
        <h1>🚀 Gmail Assistant</h1>
        <p>Service is starting up...</p>
        <p>If you see this message, the deployment is working but there's an import issue.</p>
        <a href="/test">Test Page</a>
        """
    
    @app.route('/test')
    def test():
        return "<h2>✅ Flask is working on Vercel!</h2>"

# Export the app for Vercel
# Vercel expects either 'app' or a function named 'handler'
if __name__ == "__main__":
    app.run(debug=True)
