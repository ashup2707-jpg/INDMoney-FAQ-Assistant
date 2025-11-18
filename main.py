"""
Main script to run the MoneyControl scraper
"""

from scraper import MoneyControlScraper
from data_storage import DataStorage
import json


def main():
    # Initialize scraper and storage
    scraper = MoneyControlScraper()
    storage = DataStorage()
    
    # URLs to scrape - MoneyControl
    urls = [
        "https://www.moneycontrol.com/mutual-funds/nav/hdfc-mid-cap-opportunities-fund/MHD068",
        "https://www.moneycontrol.com/mutual-funds/nav/hdfc-large-cap-fund-growth/MZU009",
        "https://www.moneycontrol.com/mutual-funds/nav/hdfc-small-cap-fund-direct-plan/MMS025"
    ]
    
    print("=" * 60)
    print("MoneyControl Mutual Fund Scraper")
    print("=" * 60)
    
    print(f"\n[1/2] Scraping {len(urls)} fund pages...")
    print("-" * 60)
    
    # Scrape all funds
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Processing: {url}")
        data = scraper.scrape_fund_page(url)
        
        if data and data.get('fund_name'):
            # Save to database
            fund_id = storage.save_fund_data(data)
            results.append(data)
            print(f"  ✓ Saved (ID: {fund_id})")
            print(f"    Fund: {data.get('fund_name', 'N/A')}")
            print(f"    Expense Ratio: {data.get('expense_ratio', 'N/A')}")
            print(f"    Returns: {data.get('returns', {})}")
        else:
            print(f"  ✗ Failed to scrape or no data extracted")
        
        print()
    
    # Save summary JSON
    with open('scraped_summary.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"[2/2] Scraping complete!")
    print(f"Successfully scraped: {len(results)} funds")
    print(f"Data saved to: mutual_funds.db")
    print(f"JSON backup saved to: data/ directory")
    print("=" * 60)


if __name__ == "__main__":
    main()

