#!/usr/bin/env python3
"""
Test client for INDMoney FAQ Assistant API
Demonstrates all API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_api():
    """Test all API endpoints"""
    
    print("\n🚀 Testing INDMoney FAQ Assistant API")
    print("="*60)
    
    try:
        # Test 1: Root endpoint
        print("\n[1] Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print_response("Root Endpoint", response)
        
        # Test 2: Get all funds
        print("\n[2] Getting all funds...")
        response = requests.get(f"{BASE_URL}/api/funds?limit=3")
        print_response("All Funds (limit 3)", response)
        
        # Test 3: Get fund detail
        print("\n[3] Getting fund detail...")
        response = requests.get(f"{BASE_URL}/api/funds/27")
        data = response.json()
        print(f"\n📊 Fund Details:")
        print(f"  Name: {data['fund_name']}")
        print(f"  Expense Ratio: {data['expense_ratio']}")
        print(f"  Returns: {data['returns']}")
        print(f"  Holdings: {len(data['holdings'])} companies")
        print(f"  FAQs: {len(data['faqs'])} questions")
        
        # Test 4: Search funds
        print("\n[4] Searching for 'small cap'...")
        response = requests.get(f"{BASE_URL}/api/search?q=small cap")
        print_response("Search Results", response)
        
        # Test 5: Search FAQs
        print("\n[5] Searching FAQs for 'expense'...")
        response = requests.get(f"{BASE_URL}/api/faq?q=expense")
        print_response("FAQ Search Results", response)
        
        # Test 6: Compare funds
        print("\n[6] Comparing funds...")
        response = requests.get(f"{BASE_URL}/api/compare?fund_ids=27,28,29")
        data = response.json()
        print(f"\n📈 Fund Comparison ({data['count']} funds):")
        for fund in data['funds']:
            print(f"\n  • {fund['fund_name']}")
            print(f"    Returns (3Y): {fund['returns'].get('3Y', 'N/A')}")
            print(f"    Expense Ratio: {fund['expense_ratio']}")
            print(f"    Risk: {fund['riskometer']}")
        
        # Test 7: Get stats
        print("\n[7] Getting database stats...")
        response = requests.get(f"{BASE_URL}/api/stats")
        print_response("Database Statistics", response)
        
        print("\n" + "="*60)
        print("✅ All tests passed successfully!")
        print("="*60)
        print("\n📚 API Documentation: http://localhost:8000/docs")
        print("🔍 Interactive Testing: http://localhost:8000/redoc")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("   Make sure the API is running: python3 api.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_api()
