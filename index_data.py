"""
Index FAQs and Funds into Vector Database
Run this script to build the RAG index
"""

from rag_service import rag_service
import sys

def main():
    print("=" * 70)
    print("🚀 INDEXING FAQS AND FUNDS INTO VECTOR DATABASE")
    print("=" * 70)
    print()
    
    if not rag_service.enabled:
        print("❌ RAG Service is not enabled")
        print("Please ensure GEMINI_API_KEY is set in your .env file")
        sys.exit(1)
    
    print("📊 Current Status:")
    print(f"   - FAQs indexed: {rag_service.faq_collection.count()}")
    print(f"   - Funds indexed: {rag_service.fund_collection.count()}")
    print()
    
    # Ask user if they want to force reindex
    if rag_service.faq_collection.count() > 0 or rag_service.fund_collection.count() > 0:
        response = input("⚠️  Data already indexed. Force reindex? (y/N): ").strip().lower()
        force_reindex = response == 'y'
    else:
        force_reindex = False
    
    print()
    print("🔄 Starting indexing process...")
    print()
    
    # Index FAQs
    print("1️⃣  Indexing FAQs...")
    faq_success = rag_service.index_faqs(force_reindex=force_reindex)
    
    # Index Funds
    print("\n2️⃣  Indexing Funds...")
    fund_success = rag_service.index_funds(force_reindex=force_reindex)
    
    print()
    print("=" * 70)
    if faq_success and fund_success:
        print("✅ INDEXING COMPLETE!")
        print()
        print(f"📋 Total FAQs indexed: {rag_service.faq_collection.count()}")
        print(f"💼 Total Funds indexed: {rag_service.fund_collection.count()}")
        print()
        print("🎉 Your RAG system is ready to use!")
    else:
        print("⚠️  INDEXING INCOMPLETE")
        print("   Check the errors above and try again")
    print("=" * 70)


if __name__ == "__main__":
    main()
