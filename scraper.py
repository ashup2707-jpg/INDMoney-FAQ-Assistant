"""
MoneyControl Mutual Fund Scraper
Extracts structured data from MoneyControl mutual fund pages with source URL tracking
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import re
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class MoneyControlScraper:
    def __init__(self, use_selenium: bool = True):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.base_url = "https://www.moneycontrol.com"
        self.scraped_data = []
        self.use_selenium = use_selenium
        self.driver = None
        
        if use_selenium:
            self._init_selenium()
        
    def _init_selenium(self):
        """Initialize Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Use webdriver-manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ Selenium WebDriver initialized successfully")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize Selenium: {e}")
            print("  Falling back to requests method...")
            self.use_selenium = False
            self.driver = None
    
    def __del__(self):
        """Clean up Selenium driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
    def _get_headers(self, referer=None):
        """Generate realistic headers to avoid blocking"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        }
        if referer:
            headers['Referer'] = referer
        return headers
    
    def _fetch_page(self, url: str, referer=None) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage using Selenium or requests"""
        if self.use_selenium and self.driver:
            return self._fetch_page_selenium(url)
        else:
            return self._fetch_page_requests(url, referer)
    
    def _fetch_page_selenium(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch page using Selenium for JavaScript rendering"""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for JavaScript to load
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            html = self.driver.page_source
            return BeautifulSoup(html, 'lxml')
        except Exception as e:
            print(f"Error fetching {url} with Selenium: {str(e)}")
            return None
    
    def _fetch_page_requests(self, url: str, referer=None) -> Optional[BeautifulSoup]:
        """Fetch page using requests (fallback)"""
        try:
            headers = self._get_headers(referer=referer or 'https://www.google.com/')
            time.sleep(1)  # Be respectful with rate limiting
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def _extract_text_from_element(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text from an element using CSS selector"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None
    
    def _extract_table_data(self, soup: BeautifulSoup) -> Dict:
        """Extract data from tables on the page"""
        tables = soup.find_all('table')
        table_data = {}
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    if key and value and key not in table_data:
                        table_data[key] = value
                
                # Also check for 3+ column tables (key-value pairs in different formats)
                if len(cells) >= 3:
                    # Sometimes data is in format: Label | Value | Additional
                    for i in range(len(cells) - 1):
                        key = cells[i].get_text(strip=True)
                        value = cells[i+1].get_text(strip=True)
                        if key and value and key not in table_data:
                            table_data[key] = value
        
        return table_data
    
    def _extract_returns(self, soup: BeautifulSoup) -> Dict:
        """Extract return data from MoneyControl"""
        returns = {}
        
        # MoneyControl stores returns in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue
            
            # Look for returns table
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    header = cells[0].get_text(strip=True)
                    
                    # Match different return periods
                    if '1 yr' in header.lower() or '1 year' in header.lower() or '1yr' in header.lower():
                        value = cells[1].get_text(strip=True)
                        if value and value != '-' and value != 'NA':
                            returns['1Y'] = value if '%' in value else value + '%'
                    
                    elif '3 yr' in header.lower() or '3 year' in header.lower() or '3yr' in header.lower():
                        value = cells[1].get_text(strip=True)
                        if value and value != '-' and value != 'NA':
                            returns['3Y'] = value if '%' in value else value + '%'
                    
                    elif '5 yr' in header.lower() or '5 year' in header.lower() or '5yr' in header.lower():
                        value = cells[1].get_text(strip=True)
                        if value and value != '-' and value != 'NA':
                            returns['5Y'] = value if '%' in value else value + '%'
        
        # Also try to find in divs with specific patterns
        text = soup.get_text()
        patterns = [
            (r'1\s*(?:Year|Yr|Y)\s*Return[\s:]*([\d.-]+)%?', '1Y'),
            (r'3\s*(?:Year|Yr|Y)\s*Return[\s:]*([\d.-]+)%?', '3Y'),
            (r'5\s*(?:Year|Yr|Y)\s*Return[\s:]*([\d.-]+)%?', '5Y'),
        ]
        
        for pattern, period in patterns:
            if period not in returns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    if value and value != '-':
                        returns[period] = value if '%' in value else value + '%'
        
        return returns
    
    def _extract_expense_ratio(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract expense ratio from MoneyControl"""
        # MoneyControl specific selectors - find text matching pattern
        expense_divs = soup.find_all(['div', 'span', 'td'])
        for div in expense_divs:
            if div.string and re.search(r'Expense Ratio', div.string, re.I):
                # Look for value in next sibling or parent
                parent = div.parent
                if parent:
                    cells = parent.find_all(['td', 'span', 'div'])
                    for cell in cells:
                        text = cell.get_text(strip=True)
                        match = re.search(r'(\d+\.?\d*)%?', text)
                        if match and match.group(1) != text.replace('Expense Ratio', '').strip():
                            return match.group(1) + '%'
        
        # Pattern matching in text
        text = soup.get_text()
        patterns = [
            r'Expense Ratio[\s:]+([\d.]+)%?',
            r'expense\s+ratio[:\s]*(\d+\.?\d*)%?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1)
                return value + '%' if '%' not in value else value
        
        # Look in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    cell_text = cells[0].get_text(strip=True).lower()
                    if 'expense' in cell_text and 'ratio' in cell_text:
                        value = cells[1].get_text(strip=True)
                        if value:
                            return value if '%' in value else value + '%'
        
        return None
    
    def _extract_exit_load(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract exit load information"""
        text = soup.get_text()
        
        # Pattern matching for exit load - more flexible
        patterns = [
            r'exit\s+load[^.]*?(\d+%?[^.]*?)(?:\.|$)',
            r'exit\s+load\s+of\s+(\d+%?)\s+if\s+redeemed[^.]*',
            r'exit\s+load[:\s]+([^\.]+?)(?:\.|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                result = match.group(0).strip()
                # Clean up the result
                if len(result) > 200:
                    result = result[:200] + '...'
                return result
        
        # Look in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    if 'exit' in cells[0].get_text(strip=True).lower() and 'load' in cells[0].get_text(strip=True).lower():
                        return cells[1].get_text(strip=True)
        
        return None
    
    def _extract_minimum_investment(self, soup: BeautifulSoup) -> Dict:
        """Extract minimum investment amounts for SIP and Lumpsum"""
        min_investment = {}
        text = soup.get_text()
        
        # Pattern matching - more flexible
        sip_patterns = [
            r'(?:SIP|sip)[^.]*?₹?\s*(\d+)',
            r'minimum[^.]*?(?:sip)[^.]*?₹?\s*(\d+)',
        ]
        lumpsum_patterns = [
            r'(?:lump\s+sum|lumpsum)[^.]*?₹?\s*(\d+)',
            r'minimum[^.]*?(?:lump|lumpsum)[^.]*?₹?\s*(\d+)',
        ]
        
        for pattern in sip_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                min_investment['SIP'] = f"₹{match.group(1)}"
                break
        
        for pattern in lumpsum_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                min_investment['Lumpsum'] = f"₹{match.group(1)}"
                break
        
        # If not found, try generic minimum
        if not min_investment:
            min_match = re.search(r'minimum[^.]*?₹?\s*(\d+)', text, re.IGNORECASE)
            if min_match:
                min_investment['Lumpsum'] = f"₹{min_match.group(1)}"
                min_investment['SIP'] = f"₹{min_match.group(1)}"  # Often same
        
        # Look in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    header = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    if 'minimum' in header or 'min investment' in header:
                        if 'sip' in header:
                            min_investment['SIP'] = value
                        else:
                            min_investment['Lumpsum'] = value
        
        return min_investment
    
    def _extract_holdings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract top holdings information"""
        holdings = []
        
        # Look for holdings table
        tables = soup.find_all('table')
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if any('holding' in h.lower() or 'stock' in h.lower() or 'company' in h.lower() for h in headers):
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        holding = {
                            'name': cells[0].get_text(strip=True),
                            'allocation': cells[1].get_text(strip=True) if len(cells) > 1 else None
                        }
                        if len(cells) > 2:
                            holding['sector'] = cells[2].get_text(strip=True)
                        holdings.append(holding)
        
        return holdings[:10]  # Top 10 holdings
    
    def _extract_fund_manager(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract fund manager name from MoneyControl"""
        # MoneyControl has fund manager in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    header = cells[0].get_text(strip=True).lower()
                    if 'fund manager' in header or 'managed by' in header:
                        return cells[1].get_text(strip=True)
        
        # Pattern matching in text
        text = soup.get_text()
        patterns = [
            r'Fund Manager[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
            r'Managed by[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                if name and len(name) > 5 and 'fund' not in name.lower():
                    return name
        
        return None
    
    def _extract_benchmark(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract benchmark information"""
        text = soup.get_text()
        
        # Pattern matching
        patterns = [
            r'benchmark[:\s]+([^\.]+?)(?:\.|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_riskometer(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract riskometer/risk level"""
        # Look for risk information
        risk_keywords = ['Very High', 'High', 'Moderate', 'Low']
        text = soup.get_text()
        
        for risk in risk_keywords:
            if risk in text:
                # Check if it's in context of risk
                pattern = f'risk[:\s]*{risk}'
                if re.search(pattern, text, re.IGNORECASE):
                    return risk
        
        # Look in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    if 'risk' in cells[0].get_text(strip=True).lower():
                        return cells[1].get_text(strip=True)
        
        return None
    
    def _extract_faqs(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract FAQ questions and answers"""
        faqs = []
        
        # Look for FAQ sections
        faq_sections = soup.find_all(['div', 'section'], class_=re.compile(r'faq|question|answer', re.I))
        
        for section in faq_sections:
            questions = section.find_all(['h3', 'h4', 'div'], class_=re.compile(r'question|faq-question', re.I))
            for q in questions:
                question = q.get_text(strip=True)
                # Find answer (usually next sibling or in same container)
                answer_elem = q.find_next(['p', 'div'], class_=re.compile(r'answer|faq-answer', re.I))
                if not answer_elem:
                    answer_elem = q.find_next_sibling(['p', 'div'])
                
                answer = answer_elem.get_text(strip=True) if answer_elem else None
                
                if question and answer:
                    faqs.append({
                        'question': question,
                        'answer': answer
                    })
        
        return faqs
    
    def _extract_lock_in(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract lock-in period (especially for ELSS)"""
        text = soup.get_text()
        
        # Pattern matching for lock-in
        patterns = [
            r'lock[-\s]?in[:\s]+(\d+)\s*(?:year|years|yr)',
            r'lock[-\s]?in\s+period[:\s]+(\d+)\s*(?:year|years|yr)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)} years"
        
        # Check if ELSS (which has 3 year lock-in)
        if 'ELSS' in text or 'tax saver' in text.lower():
            return "3 years (ELSS)"
        
        return None
    
    def _extract_peer_comparison(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract peer comparison data if available"""
        # Look for comparison tables or sections
        comparison_section = soup.find(['div', 'section'], class_=re.compile(r'comparison|peer|compare', re.I))
        
        if comparison_section:
            # Extract comparison data
            return {
                'data': comparison_section.get_text(strip=True)
            }
        
        return None
    
    def scrape_fund_page(self, url: str) -> Optional[Dict]:
        """Scrape a single mutual fund page from MoneyControl"""
        print(f"Scraping: {url}")
        soup = self._fetch_page(url)
        
        if not soup:
            return None
        
        # Extract fund name - MoneyControl has it in title and h1
        fund_name = None
        
        # Try h1 first (most common on MoneyControl)
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = h1.get_text(strip=True)
            if text and len(text) > 5 and 'mutual fund' not in text.lower():
                fund_name = text
                break
        
        # Try title tag
        if not fund_name:
            title = soup.find('title')
            if title:
                title_text = title.get_text(strip=True)
                # Clean up title (MoneyControl adds extra text)
                fund_name = title_text.replace('NAV', '').replace('Latest & Historical NAV', '').replace('- Moneycontrol', '').strip()
        
        # Fallback: Extract from URL
        if not fund_name:
            url_parts = url.split('/')
            if len(url_parts) > 0:
                last_part = url_parts[-2] if len(url_parts) > 1 else url_parts[-1]
                fund_name = last_part.replace('-', ' ').title()
        
        # Clean fund name
        if fund_name:
            fund_name = ' '.join(fund_name.split())
        
        # Extract all data
        fund_data = {
            'source_url': url,
            'fund_name': fund_name,
            'expense_ratio': self._extract_expense_ratio(soup),
            'exit_load': self._extract_exit_load(soup),
            'minimum_investment': self._extract_minimum_investment(soup),
            'returns': self._extract_returns(soup),
            'holdings': self._extract_holdings(soup),
            'fund_manager': self._extract_fund_manager(soup),
            'benchmark': self._extract_benchmark(soup),
            'riskometer': self._extract_riskometer(soup),
            'lock_in': self._extract_lock_in(soup),
            'peer_comparison': self._extract_peer_comparison(soup),
            'faqs': self._extract_faqs(soup),
            'table_data': self._extract_table_data(soup),
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return fund_data
    
    def scrape_amc_page(self, url: str) -> List[str]:
        """Scrape AMC page to get list of fund URLs"""
        print(f"Scraping AMC page: {url}")
        soup = self._fetch_page(url)
        
        if not soup:
            return []
        
        fund_urls = []
        
        # Find all links to mutual fund pages
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            if href and isinstance(href, str) and '/mutual-funds/' in href:
                # Convert relative URLs to absolute
                full_url = urljoin(self.base_url, href)
                if full_url not in fund_urls:
                    fund_urls.append(full_url)
        
        return fund_urls
    
    def scrape_multiple_funds(self, urls: List[str]) -> List[Dict]:
        """Scrape multiple fund pages"""
        results = []
        
        for url in urls:
            data = self.scrape_fund_page(url)
            if data:
                results.append(data)
            time.sleep(2)  # Be respectful with rate limiting
        
        return results
    
    def save_data(self, filename: str = 'scraped_data.json'):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")


if __name__ == "__main__":
    scraper = MoneyControlScraper()
    
    # URLs to scrape - MoneyControl
    urls = [
        "https://www.moneycontrol.com/mutual-funds/nav/hdfc-mid-cap-opportunities-fund/MHD068",
        "https://www.moneycontrol.com/mutual-funds/nav/hdfc-large-cap-fund-growth/MZU009",
        "https://www.moneycontrol.com/mutual-funds/nav/hdfc-small-cap-fund-direct-plan/MMS025"
    ]
    
    print(f"Scraping {len(urls)} fund URLs")
    
    # Scrape all funds
    results = scraper.scrape_multiple_funds(urls)
    scraper.scraped_data = results
    
    # Save data
    scraper.save_data('scraped_data.json')
    
    print(f"\nScraped {len(results)} funds successfully!")

