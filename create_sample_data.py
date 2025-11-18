#!/usr/bin/env python3
"""
Create sample mutual fund data for testing the application
This allows you to continue development while scraping issues are resolved
"""

from data_storage import DataStorage
import json
from datetime import datetime

# Sample realistic data for HDFC funds
sample_funds = [
    {
        "source_url": "https://www.moneycontrol.com/mutual-funds/nav/hdfc-mid-cap-opportunities-fund/MHD068",
        "fund_name": "HDFC Mid Cap Opportunities Fund - Direct Plan - Growth",
        "expense_ratio": "0.75%",
        "exit_load": "1% if redeemed within 1 year",
        "minimum_investment": {
            "SIP": "₹500",
            "Lumpsum": "₹5000"
        },
        "returns": {
            "1Y": "28.5%",
            "3Y": "24.3%",
            "5Y": "22.1%"
        },
        "holdings": [
            {"name": "Infosys Ltd", "allocation": "4.2%", "sector": "Technology"},
            {"name": "ICICI Bank Ltd", "allocation": "3.8%", "sector": "Banking"},
            {"name": "Bajaj Finance Ltd", "allocation": "3.5%", "sector": "Financial Services"},
            {"name": "Axis Bank Ltd", "allocation": "3.2%", "sector": "Banking"},
            {"name": "Sun Pharma Industries", "allocation": "2.9%", "sector": "Pharmaceuticals"}
        ],
        "fund_manager": "Chirag Setalvad",
        "benchmark": "Nifty Midcap 150 TRI",
        "riskometer": "Very High",
        "lock_in": None,
        "peer_comparison": None,
        "faqs": [
            {
                "question": "What is the minimum SIP amount for this fund?",
                "answer": "The minimum SIP amount is ₹500 per month."
            },
            {
                "question": "What is the expense ratio?",
                "answer": "The expense ratio for the direct plan is 0.75%."
            }
        ],
        "table_data": {
            "NAV": "₹145.32",
            "AUM": "₹45,234 Cr",
            "Fund Age": "12 years",
            "Category": "Mid Cap Fund"
        },
        "scraped_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        "source_url": "https://www.moneycontrol.com/mutual-funds/nav/hdfc-large-cap-fund-growth/MZU009",
        "fund_name": "HDFC Top 100 Fund - Direct Plan - Growth",
        "expense_ratio": "0.65%",
        "exit_load": "1% if redeemed within 1 year",
        "minimum_investment": {
            "SIP": "₹500",
            "Lumpsum": "₹5000"
        },
        "returns": {
            "1Y": "22.3%",
            "3Y": "18.7%",
            "5Y": "16.5%"
        },
        "holdings": [
            {"name": "Reliance Industries", "allocation": "8.5%", "sector": "Energy"},
            {"name": "HDFC Bank", "allocation": "7.2%", "sector": "Banking"},
            {"name": "Infosys Ltd", "allocation": "6.1%", "sector": "Technology"},
            {"name": "TCS Ltd", "allocation": "5.8%", "sector": "Technology"},
            {"name": "ITC Ltd", "allocation": "4.9%", "sector": "FMCG"}
        ],
        "fund_manager": "Rakesh Vyas",
        "benchmark": "Nifty 100 TRI",
        "riskometer": "Moderately High",
        "lock_in": None,
        "peer_comparison": None,
        "faqs": [
            {
                "question": "What type of companies does this fund invest in?",
                "answer": "This fund primarily invests in large-cap companies from the Nifty 100 index."
            },
            {
                "question": "Is this suitable for long-term investment?",
                "answer": "Yes, this is ideal for investors with a 5+ year investment horizon."
            }
        ],
        "table_data": {
            "NAV": "₹892.45",
            "AUM": "₹67,891 Cr",
            "Fund Age": "15 years",
            "Category": "Large Cap Fund"
        },
        "scraped_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        "source_url": "https://www.moneycontrol.com/mutual-funds/nav/hdfc-small-cap-fund-direct-plan/MMS025",
        "fund_name": "HDFC Small Cap Fund - Direct Plan - Growth",
        "expense_ratio": "0.85%",
        "exit_load": "1% if redeemed within 1 year",
        "minimum_investment": {
            "SIP": "₹500",
            "Lumpsum": "₹5000"
        },
        "returns": {
            "1Y": "35.2%",
            "3Y": "28.9%",
            "5Y": "25.4%"
        },
        "holdings": [
            {"name": "Dixon Technologies", "allocation": "2.1%", "sector": "Electronics"},
            {"name": "Kalyan Jewellers", "allocation": "1.9%", "sector": "Retail"},
            {"name": "PB Fintech", "allocation": "1.7%", "sector": "Financial Services"},
            {"name": "Zomato Ltd", "allocation": "1.6%", "sector": "Consumer Services"},
            {"name": "Delhivery Ltd", "allocation": "1.5%", "sector": "Logistics"}
        ],
        "fund_manager": "Chirag Setalvad",
        "benchmark": "Nifty Smallcap 250 TRI",
        "riskometer": "Very High",
        "lock_in": None,
        "peer_comparison": None,
        "faqs": [
            {
                "question": "What is the risk level of this fund?",
                "answer": "This fund has a Very High risk rating as it invests in small-cap companies."
            },
            {
                "question": "Who should invest in this fund?",
                "answer": "Investors with high risk appetite and 7+ year investment horizon."
            }
        ],
        "table_data": {
            "NAV": "₹234.67",
            "AUM": "₹28,456 Cr",
            "Fund Age": "10 years",
            "Category": "Small Cap Fund"
        },
        "scraped_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
]

def create_sample_data():
    """Create sample data in database"""
    storage = DataStorage()
    
    print("=" * 60)
    print("Creating Sample Mutual Fund Data")
    print("=" * 60)
    print()
    
    for i, fund_data in enumerate(sample_funds, 1):
        print(f"[{i}/{len(sample_funds)}] Creating: {fund_data['fund_name']}")
        fund_id = storage.save_fund_data(fund_data)
        print(f"  ✓ Saved with ID: {fund_id}")
        print(f"    Expense Ratio: {fund_data['expense_ratio']}")
        print(f"    Returns: {fund_data['returns']}")
        print()
    
    # Save summary JSON
    with open('sample_data_summary.json', 'w', encoding='utf-8') as f:
        json.dump(sample_funds, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print("✓ Sample data created successfully!")
    print(f"  Total funds: {len(sample_funds)}")
    print(f"  Database: mutual_funds.db")
    print(f"  JSON backup: data/ directory")
    print(f"  Summary: sample_data_summary.json")
    print("=" * 60)
    print()
    print("You can now:")
    print("  1. Test query functions: python3 query_funds.py")
    print("  2. Build your backend API")
    print("  3. Develop the frontend")
    print("  4. Work on FAQ features")

if __name__ == "__main__":
    create_sample_data()
