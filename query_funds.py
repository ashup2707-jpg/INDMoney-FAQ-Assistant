"""
Query script to display top HDFC funds
"""

from data_storage import DataStorage
import json


def display_top_funds(storage: DataStorage, limit: int = 10):
    """Display top HDFC funds by AUM or returns"""
    all_funds = storage.get_all_funds()
    
    if not all_funds:
        print("No funds found in database. Please run the scraper first.")
        return
    
    # Filter HDFC funds
    hdfc_funds = [f for f in all_funds if 'hdfc' in f.get('fund_name', '').lower()]
    
    if not hdfc_funds:
        print("No HDFC funds found. Showing all funds:")
        hdfc_funds = all_funds
    
    print("=" * 80)
    print(f"TOP {limit} HDFC MUTUAL FUNDS")
    print("=" * 80)
    print()
    
    # Sort by AUM if available, otherwise by fund name
    def get_aum_value(fund):
        aum = fund.get('aum', '')
        if not aum:
            return 0
        # Extract numeric value from strings like "₹89,383Cr" or "₹1,06,493Cr"
        try:
            aum_clean = aum.replace('₹', '').replace(',', '').replace('Cr', '').strip()
            return float(aum_clean) if aum_clean else 0
        except:
            return 0
    
    sorted_funds = sorted(hdfc_funds, key=get_aum_value, reverse=True)[:limit]
    
    for i, fund in enumerate(sorted_funds, 1):
        print(f"{i}. {fund.get('fund_name', 'N/A')}")
        print(f"   Source: {fund.get('source_url', 'N/A')}")
        print(f"   Expense Ratio: {fund.get('expense_ratio', 'N/A')}")
        print(f"   Exit Load: {fund.get('exit_load', 'N/A')}")
        print(f"   Riskometer: {fund.get('riskometer', 'N/A')}")
        print(f"   AUM: {fund.get('aum', 'N/A')}")
        
        # Get returns
        import sqlite3
        conn = sqlite3.connect(storage.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT period, return_value FROM returns WHERE fund_id = ?', (fund['id'],))
        returns = {r['period']: r['return_value'] for r in cursor.fetchall()}
        conn.close()
        
        if returns:
            returns_str = ', '.join([f"{k}: {v}" for k, v in returns.items()])
            print(f"   Returns: {returns_str}")
        
        print(f"   Minimum SIP: {fund.get('minimum_sip', 'N/A')}")
        print(f"   Minimum Lumpsum: {fund.get('minimum_lumpsum', 'N/A')}")
        if fund.get('lock_in'):
            print(f"   Lock-in: {fund.get('lock_in')}")
        print()


if __name__ == "__main__":
    storage = DataStorage()
    display_top_funds(storage, limit=10)

