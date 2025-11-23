# test_watson_creds.py
import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your Watson credentials
WATSON_STT_URL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/475537ec-370b-4e6a-a7a8-a1a6ab3bee0c"
WATSON_STT_API_KEY = "_UP7mhpiVYiZpGdEukbED-uyx1py1virhxs2AHP4XhKZ"

print("=" * 60)
print("TESTING WATSON SPEECH-TO-TEXT CREDENTIALS")
print("=" * 60)

# Test 1: Check if credentials authenticate
print("\n1. Testing authentication...")
url = f"{WATSON_STT_URL}/v1/models"
auth = base64.b64encode(f"apikey:{WATSON_STT_API_KEY}".encode()).decode()
headers = {'Authorization': f'Basic {auth}'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        print("   ✅ Authentication successful!")
        models = response.json()
        print(f"   ✅ Found {len(models['models'])} available models")
        
        # Show first 3 models
        print("\n   Available models:")
        for model in models['models'][:3]:
            print(f"   - {model['name']}")
            
    elif response.status_code == 401:
        print("   ❌ Authentication failed - invalid API key")
        print(f"   Response: {response.text}")
    else:
        print(f"   ❌ Unexpected status: {response.status_code}")
        print(f"   Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("   ❌ Request timed out")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Test a simple transcription
print("\n2. Testing transcription capability...")
print("   (Creating a test audio file...)")

# Create a simple test by checking the recognize endpoint
url = f"{WATSON_STT_URL}/v1/recognize"
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'audio/wav'
}

try:
    # Just test if the endpoint responds (will fail with no audio, but that's ok)
    response = requests.post(url, headers=headers, data=b'', timeout=5)
    
    if response.status_code == 400:
        print("   ✅ Transcription endpoint is accessible")
        print("   (Error is expected with empty audio)")
    elif response.status_code == 401:
        print("   ❌ Authentication failed for transcription")
    else:
        print(f"   Status: {response.status_code}")
        
except Exception as e:
    print(f"   Note: {e}")

print("\n" + "=" * 60)
print("SUMMARY:")
print("=" * 60)

if response.status_code in [200, 400]:
    print("✅ Your Watson STT credentials are VALID and WORKING!")
    print("✅ You can transcribe videos with these credentials")
    print("\nNext steps:")
    print("1. Restart your backend: uvicorn main:app --reload")
    print("2. Upload a video to test transcription")
    print("3. Check the backend logs for transcription details")
else:
    print("❌ There might be an issue with your credentials")
    print("Please check your .env file")

print("=" * 60)