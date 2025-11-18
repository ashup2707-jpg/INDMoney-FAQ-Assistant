#!/usr/bin/env python3
"""
Quick setup script for Gemini API key
"""

import os

print("="*60)
print("  Gemini API Key Setup")
print("="*60)
print()
print("Get your FREE Gemini API key:")
print("1. Visit: https://makersuite.google.com/app/apikey")
print("2. Sign in with your Google account")
print("3. Click 'Get API Key'")
print("4. Create API key in new or existing project")
print("5. Copy the key")
print()

api_key = input("Paste your Gemini API key here: ").strip()

if api_key:
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"GEMINI_API_KEY={api_key}\n")
    
    print()
    print("✓ API key saved to .env file")
    print()
    print("You can now:")
    print("  1. Restart the API: python3 api.py")
    print("  2. Test Gemini: python3 gemini_service.py")
    print()
else:
    print("\n✗ No API key provided")
    print("Run this script again when you have your API key")
