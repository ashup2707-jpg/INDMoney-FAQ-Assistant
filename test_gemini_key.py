import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"🔑 API Key loaded: {api_key[:20]}..." if api_key else "❌ No API key found")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        print("\n🧪 Testing Gemini API...")
        response = model.generate_content("Say 'Hello from INDMoney!' in one sentence.")
        
        print(f"✅ SUCCESS! Gemini API is working!")
        print(f"📝 Response: {response.text}")
        print(f"\n🎉 Your API key is valid and ready to use!")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("\n⚠️  The API key might be invalid or expired.")
else:
    print("❌ No API key found in .env file")
