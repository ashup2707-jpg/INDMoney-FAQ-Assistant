INDMoney FAQ Assistant - Setup Guide
=====================================

INSTALLATION:
1. Install Python 3.8 or higher
2. Install dependencies:
   pip install -r requirements.txt

USAGE:
1. Run the scraper:
   python main.py

2. The scraper will:
   - Scrape the provided Groww URLs
   - Extract mutual fund data
   - Store in SQLite database (mutual_funds.db)
   - Save JSON backups in data/ directory

DATA EXTRACTED:
- Expense Ratio
- Exit Load
- Minimum SIP/Lumpsum Investment
- Returns (1Y, 3Y, 5Y)
- Top Holdings
- Fund Manager
- Benchmark
- Riskometer
- Lock-in Period (for ELSS)
- Peer Comparison
- FAQs
- Source URL (for attribution)

STORAGE:
- SQLite database: mutual_funds.db
- JSON backups: data/ directory
- All data includes source_url for attribution

