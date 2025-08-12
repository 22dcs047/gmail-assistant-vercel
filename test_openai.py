import os
from dotenv import load_dotenv
load_dotenv()

try:
    import openai
    print("✅ OpenAI imported successfully")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ API key found")
        
        # Try new OpenAI client
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
        
        # Test simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ OpenAI connection test successful!")
        
    else:
        print("❌ API key not found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("Trying to fix OpenAI installation...")
    import subprocess
    subprocess.check_call(['pip', 'install', '--upgrade', 'openai'])
    print("Please run this test again")
