"""
Test script to query specific fund information from MoneyControl
"""

from scraper import MoneyControlScraper
from data_storage import DataStorage
import json

def test_queries():
    scraper = MoneyControlScraper()
    storage = DataStorage()
    
    # Fund URLs - MoneyControl
    funds = {
        'mid_cap': 'https://www.moneycontrol.com/mutual-funds/nav/hdfc-mid-cap-opportunities-fund/MHD068',
        'large_cap': 'https://www.moneycontrol.com/mutual-funds/nav/hdfc-large-cap-fund-growth/MZU009',
        'small_cap': 'https://www.moneycontrol.com/mutual-funds/nav/hdfc-small-cap-fund-direct-plan/MMS025'
    }
    
    print("=" * 80)
    print("TESTING SCRAPER - SPECIFIC QUERIES")
    print("=" * 80)
    print()
    
    results = {}
    
    # Test 1: 3 year return of mid cap fund
    print("[TEST 1] Scraping 3-year return of HDFC Mid Cap Fund...")
    print("-" * 80)
    mid_cap_data = scraper.scrape_fund_page(funds['mid_cap'])
    if mid_cap_data:
        storage.save_fund_data(mid_cap_data)
        results['mid_cap'] = mid_cap_data
        
        print(f"Fund: {mid_cap_data.get('fund_name', 'N/A')}")
        print(f"Source: {mid_cap_data.get('source_url', 'N/A')}")
        returns = mid_cap_data.get('returns', {})
        print(f"Returns: {returns}")
        if '3Y' in returns:
            print(f"✓ 3-Year Return: {returns['3Y']}")
        else:
            print("✗ 3-Year Return: Not found")
            print("  Available returns:", list(returns.keys()))
    else:
        print("✗ Failed to scrape fund")
    print()
    
    # Test 2: Expense ratio of large cap fund
    print("[TEST 2] Scraping expense ratio of HDFC Large Cap Fund...")
    print("-" * 80)
    large_cap_data = scraper.scrape_fund_page(funds['large_cap'])
    if large_cap_data:
        storage.save_fund_data(large_cap_data)
        results['large_cap'] = large_cap_data
        
        print(f"Fund: {large_cap_data.get('fund_name', 'N/A')}")
        print(f"Source: {large_cap_data.get('source_url', 'N/A')}")
        expense_ratio = large_cap_data.get('expense_ratio')
        if expense_ratio:
            print(f"✓ Expense Ratio: {expense_ratio}")
        else:
            print("✗ Expense Ratio: Not found")
            print("  Raw data keys:", list(large_cap_data.keys()))
    else:
        print("✗ Failed to scrape fund")
    print()
    
    # Test 3: Fund manager of small cap fund
    print("[TEST 3] Scraping fund manager of HDFC Small Cap Fund...")
    print("-" * 80)
    small_cap_data = scraper.scrape_fund_page(funds['small_cap'])
    if small_cap_data:
        storage.save_fund_data(small_cap_data)
        results['small_cap'] = small_cap_data
        
        print(f"Fund: {small_cap_data.get('fund_name', 'N/A')}")
        print(f"Source: {small_cap_data.get('source_url', 'N/A')}")
        fund_manager = small_cap_data.get('fund_manager')
        if fund_manager:
            print(f"✓ Fund Manager: {fund_manager}")
        else:
            print("✗ Fund Manager: Not found")
            print("  Raw data keys:", list(small_cap_data.keys()))
    else:
        print("✗ Failed to scrape fund")
    print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    if 'mid_cap' in results:
        returns = results['mid_cap'].get('returns', {})
        print(f"1. 3-Year Return (Mid Cap): {returns.get('3Y', 'Not found')}")
        print(f"   Source: {results['mid_cap'].get('source_url')}")
    
    if 'large_cap' in results:
        print(f"2. Expense Ratio (Large Cap): {results['large_cap'].get('expense_ratio', 'Not found')}")
        print(f"   Source: {results['large_cap'].get('source_url')}")
    
    if 'small_cap' in results:
        print(f"3. Fund Manager (Small Cap): {results['small_cap'].get('fund_manager', 'Not found')}")
        print(f"   Source: {results['small_cap'].get('source_url')}")
    
    print()
    print("=" * 80)
    
    # Save detailed results
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Detailed results saved to: test_results.json")

if __name__ == "__main__":
    test_queries()

