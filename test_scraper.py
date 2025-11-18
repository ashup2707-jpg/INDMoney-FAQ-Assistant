"""
Test scraper to debug extraction from MoneyControl
"""

from scraper import MoneyControlScraper
import json

scraper = MoneyControlScraper(use_selenium=True)  # Enable Selenium
url = "https://www.moneycontrol.com/mutual-funds/nav/hdfc-mid-cap-opportunities-fund/MHD068"

print("Testing scraper...")
data = scraper.scrape_fund_page(url)

if data:
    print("\nExtracted Data:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print("No data extracted")
    
    # Debug: Check what we got
    soup = scraper._fetch_page(url)
    if soup:
        title_tag = soup.find('title')
        print("\nPage title:", title_tag.text if title_tag else 'No title')
        print("\nH1 tags:")
        for h1 in soup.find_all('h1'):
            print(f"  - {h1.get_text(strip=True)}")
        
        print("\nTables found:", len(soup.find_all('table')))
        print("\nFirst table structure:")
        first_table = soup.find('table')
        if first_table:
            rows = first_table.find_all('tr')[:5]
            for row in rows:
                cells = row.find_all(['td', 'th'])
                print(f"  Row: {[c.get_text(strip=True)[:50] for c in cells]}")
