# Quick Setup Script for Enhanced Gmail Assistant
# Run this to get everything working with real Gmail + OpenAI

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "="*60)
    print(f"🚀 {text}")
    print("="*60)

def print_step(step, text):
    print(f"\n📋 Step {step}: {text}")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def check_file_exists(filepath, description):
    if os.path.exists(filepath):
        print_success(f"{description} found: {filepath}")
        return True
    else:
        print_error(f"{description} NOT found: {filepath}")
        return False

def install_packages():
    """Install required packages"""
    packages = [
        "openai==1.12.0",
        "python-dotenv==1.0.0",
        "Flask==2.3.3",
        "google-auth==2.23.3",
        "google-auth-oauthlib==1.0.0", 
        "google-auth-httplib2==0.1.1",
        "google-api-python-client==2.103.0"
    ]
    
    print_step(1, "Installing Required Packages")
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print_success(f"Installed {package}")
        except subprocess.CalledProcessError:
            print_error(f"Failed to install {package}")
            return False
    
    print_success("All packages installed successfully!")
    return True

def setup_environment():
    """Set up environment file"""
    print_step(2, "Setting Up Environment Variables")
    
    # Check if .env exists
    env_path = ".env"
    if os.path.exists(env_path):
        print_warning(".env file already exists")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            return True
    
    # Get OpenAI API key
    print("\n🔑 OpenAI API Key Setup:")
    print("1. Go to https://platform.openai.com/")
    print("2. Sign up or login")
    print("3. Go to API Keys section")
    print("4. Create new secret key")
    print("5. Copy the key (starts with sk-)")
    
    api_key = input("\nEnter your OpenAI API key: ").strip()
    
    if not api_key.startswith("sk-"):
        print_error("Invalid API key format. Should start with 'sk-'")
        return False
    
    # Create .env file
    env_content = f"""# OpenAI Configuration
OPENAI_API_KEY={api_key}

# Gmail Configuration
GMAIL_USER_EMAIL=22dcs047@charusat.edu.in

# Application Settings
ENVIRONMENT=production
DEBUG=False
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print_success(f"Environment file created: {env_path}")
        return True
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return False

def check_gmail_credentials():
    """Check Gmail API credentials"""
    print_step(3, "Checking Gmail API Credentials")
    
    # Check for credentials in multiple locations
    locations = [
        "credentials.json",
        "api/credentials.json", 
        "../credentials.json"
    ]
    
    creds_found = False
    token_found = False
    
    for location in locations:
        if check_file_exists(location, "Gmail credentials.json"):
            creds_found = True
            break
    
    # Check for token
    token_locations = [
        "token.json",
        "api/token.json",
        "../token.json" 
    ]
    
    for location in token_locations:
        if check_file_exists(location, "Gmail token.json"):
            token_found = True
            break
    
    if not creds_found:
        print_error("Gmail credentials.json not found!")
        print("Please ensure credentials.json is in the project directory")
        return False
    
    if not token_found:
        print_warning("Gmail token.json not found - you may need to re-authenticate")
        print("The app will prompt for authentication on first run")
    
    return True

def test_connections():
    """Test OpenAI and Gmail connections"""
    print_step(4, "Testing Connections")
    
    # Test OpenAI
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print_error("OpenAI API key not found in environment")
            return False
        
        client = openai.OpenAI(api_key=api_key)
        
        # Test with minimal request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=5
        )
        print_success("OpenAI connection successful!")
        
    except Exception as e:
        print_error(f"OpenAI connection failed: {e}")
        return False
    
    # Test Gmail (basic import check)
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        print_success("Gmail API libraries available!")
    except ImportError as e:
        print_error(f"Gmail API libraries not available: {e}")
        return False
    
    return True

def create_run_script():
    """Create a simple run script"""
    print_step(5, "Creating Run Script")
    
    run_script = """# Simple run script for Gmail Assistant
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced app
try:
    from api.app import app, gmail_assistant
    
    print("🚀 Starting Enhanced Gmail Assistant...")
    print(f"📧 Gmail Connected: {bool(gmail_assistant.gmail_service)}")
    print(f"🧠 OpenAI Connected: {bool(gmail_assistant.openai_client)}")
    print("🌐 Visit: http://localhost:5000")
    print("🔍 Debug: http://localhost:5000/debug")
    
    app.run(debug=True, port=5000)
    
except Exception as e:
    print(f"❌ Error starting app: {e}")
    print("Please check your setup and try again.")
"""
    
    try:
        with open("run_assistant.py", 'w') as f:
            f.write(run_script)
        print_success("Run script created: run_assistant.py")
        return True
    except Exception as e:
        print_error(f"Failed to create run script: {e}")
        return False

def main():
    print_header("Enhanced Gmail Assistant Setup")
    print("This will set up real Gmail + OpenAI integration")
    
    # Step 1: Install packages
    if not install_packages():
        print_error("Package installation failed. Please install manually.")
        return
    
    # Step 2: Set up environment
    if not setup_environment():
        print_error("Environment setup failed.")
        return
    
    # Step 3: Check Gmail credentials  
    if not check_gmail_credentials():
        print_error("Gmail credentials check failed.")
        return
    
    # Step 4: Test connections
    if not test_connections():
        print_error("Connection tests failed.")
        return
    
    # Step 5: Create run script
    if not create_run_script():
        print_error("Run script creation failed.")
        return
    
    # Success!
    print_header("Setup Complete! 🎉")
    print("✅ All packages installed")
    print("✅ Environment configured") 
    print("✅ OpenAI connection tested")
    print("✅ Gmail API ready")
    print("✅ Run script created")
    
    print("\n🚀 Next Steps:")
    print("1. Run: python run_assistant.py")
    print("2. Visit: http://localhost:5000")
    print("3. Check status: http://localhost:5000/debug")
    print("4. Use dashboard: http://localhost:5000/dashboard")
    
    print("\n🎯 Expected Results:")
    print("- Real Gmail emails in dashboard")
    print("- AI classification badges on emails") 
    print("- Smart auto-reply generation")
    print("- Real drafts created in Gmail")
    
    print("\n📚 If you have issues:")
    print("- Check .env file has correct OpenAI key")
    print("- Ensure credentials.json is in project folder")
    print("- Visit /debug page for detailed status")

if __name__ == "__main__":
    main()
