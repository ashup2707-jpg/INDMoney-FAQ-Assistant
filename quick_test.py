#!/usr/bin/env python3
"""Quick test to verify Selenium setup"""

import sys
print("Starting quick test...")

try:
    from scraper import MoneyControlScraper
    print("✓ Scraper module imported")
    
    print("\nInitializing scraper with Selenium...")
    scraper = MoneyControlScraper(use_selenium=True)
    
    if scraper.driver:
        print("✓ Selenium WebDriver is working!")
        print(f"  Driver type: {type(scraper.driver)}")
        
        # Try a simple fetch
        print("\nTesting page fetch...")
        url = "https://www.moneycontrol.com/mutual-funds/nav/hdfc-mid-cap-opportunities-fund/MHD068"
        soup = scraper._fetch_page(url)
        
        if soup:
            print(f"✓ Page fetched successfully!")
            print(f"  Page title: {soup.find('title').text if soup.find('title') else 'No title'}")
            print(f"  Tables found: {len(soup.find_all('table'))}")
        else:
            print("✗ Failed to fetch page")
            
        # Cleanup
        scraper.driver.quit()
    else:
        print("✗ Selenium WebDriver failed to initialize")
        print("  The scraper will use requests as fallback")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Test complete!")
