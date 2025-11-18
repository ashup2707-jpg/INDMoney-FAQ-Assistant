"""
Test RAG System with Semantic Queries
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_query(question):
    print(f"\n{'='*70}")
    print(f"📝 QUESTION: {question}")
    print('='*70)
    
    try:
        response = requests.post(
            f"{API_BASE}/api/ai/ask",
            json={"question": question, "use_context": True},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n💡 ANSWER:")
            print(result['answer'])
            print(f"\n🔍 Retrieval Method: {result.get('retrieval_method', 'unknown')}")
            print(f"🤖 Source: {result['source']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("\n" + "="*70)
    print("🚀 TESTING RAG SYSTEM WITH SEMANTIC QUERIES")
    print("="*70)
    
    # Test semantic search capabilities
    test_queries = [
        # Direct questions from FAQs
        "What is the minimum SIP amount?",
        "Tell me about exit load",
        
        # Semantic variations (should find similar FAQs)
        "How much money do I need to start investing monthly?",  # Similar to minimum SIP
        "What happens if I withdraw early?",  # Similar to exit load
        
        # Fund-specific questions
        "Which fund is best for mid-cap investing?",
        "Compare HDFC mid cap and small cap funds",
        
        # Investment advice
        "I want to invest ₹10000 per month for 5 years with moderate risk",
        
        # Term explanation
        "What does expense ratio mean?",
    ]
    
    for query in test_queries:
        test_query(query)
    
    print("\n" + "="*70)
    print("✅ RAG TESTING COMPLETE!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
