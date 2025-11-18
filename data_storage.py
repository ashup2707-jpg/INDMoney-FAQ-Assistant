"""
Data Storage Module
Handles storing scraped data with source URL tracking
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import sqlite3


class DataStorage:
    def __init__(self, db_path: str = 'mutual_funds.db', json_path: str = 'data'):
        self.db_path = db_path
        self.json_path = json_path
        os.makedirs(self.json_path, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create funds table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_name TEXT,
                source_url TEXT UNIQUE,
                expense_ratio TEXT,
                exit_load TEXT,
                minimum_sip TEXT,
                minimum_lumpsum TEXT,
                fund_manager TEXT,
                benchmark TEXT,
                riskometer TEXT,
                lock_in TEXT,
                nav TEXT,
                aum TEXT,
                scraped_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create returns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS returns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_id INTEGER,
                period TEXT,
                return_value TEXT,
                source_url TEXT,
                FOREIGN KEY (fund_id) REFERENCES funds(id)
            )
        ''')
        
        # Create holdings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS holdings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_id INTEGER,
                holding_name TEXT,
                allocation TEXT,
                sector TEXT,
                source_url TEXT,
                FOREIGN KEY (fund_id) REFERENCES funds(id)
            )
        ''')
        
        # Create FAQs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_id INTEGER,
                question TEXT,
                answer TEXT,
                source_url TEXT,
                FOREIGN KEY (fund_id) REFERENCES funds(id)
            )
        ''')
        
        # Create peer comparison table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peer_comparison (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_id INTEGER,
                comparison_data TEXT,
                source_url TEXT,
                FOREIGN KEY (fund_id) REFERENCES funds(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_fund_data(self, fund_data: Dict) -> int:
        """Save fund data to database and return fund_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert or update fund
        cursor.execute('''
            INSERT OR REPLACE INTO funds 
            (fund_name, source_url, expense_ratio, exit_load, minimum_sip, 
             minimum_lumpsum, fund_manager, benchmark, riskometer, lock_in, 
             nav, aum, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fund_data.get('fund_name'),
            fund_data.get('source_url'),
            fund_data.get('expense_ratio'),
            fund_data.get('exit_load'),
            fund_data.get('minimum_investment', {}).get('SIP'),
            fund_data.get('minimum_investment', {}).get('Lumpsum'),
            fund_data.get('fund_manager'),
            fund_data.get('benchmark'),
            fund_data.get('riskometer'),
            fund_data.get('lock_in'),
            fund_data.get('table_data', {}).get('NAV'),
            fund_data.get('table_data', {}).get('AUM'),
            fund_data.get('scraped_at')
        ))
        
        fund_id = cursor.lastrowid
        
        # Save returns
        if fund_data.get('returns'):
            cursor.execute('DELETE FROM returns WHERE fund_id = ?', (fund_id,))
            for period, value in fund_data['returns'].items():
                cursor.execute('''
                    INSERT INTO returns (fund_id, period, return_value, source_url)
                    VALUES (?, ?, ?, ?)
                ''', (fund_id, period, value, fund_data.get('source_url')))
        
        # Save holdings
        if fund_data.get('holdings'):
            cursor.execute('DELETE FROM holdings WHERE fund_id = ?', (fund_id,))
            for holding in fund_data['holdings']:
                cursor.execute('''
                    INSERT INTO holdings (fund_id, holding_name, allocation, sector, source_url)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    fund_id,
                    holding.get('name'),
                    holding.get('allocation'),
                    holding.get('sector'),
                    fund_data.get('source_url')
                ))
        
        # Save FAQs
        if fund_data.get('faqs'):
            cursor.execute('DELETE FROM faqs WHERE fund_id = ?', (fund_id,))
            for faq in fund_data['faqs']:
                cursor.execute('''
                    INSERT INTO faqs (fund_id, question, answer, source_url)
                    VALUES (?, ?, ?, ?)
                ''', (
                    fund_id,
                    faq.get('question'),
                    faq.get('answer'),
                    fund_data.get('source_url')
                ))
        
        # Save peer comparison
        if fund_data.get('peer_comparison'):
            cursor.execute('DELETE FROM peer_comparison WHERE fund_id = ?', (fund_id,))
            cursor.execute('''
                INSERT INTO peer_comparison (fund_id, comparison_data, source_url)
                VALUES (?, ?, ?)
            ''', (
                fund_id,
                json.dumps(fund_data['peer_comparison']),
                fund_data.get('source_url')
            ))
        
        conn.commit()
        conn.close()
        
        # Also save as JSON for backup
        self._save_json(fund_data)
        
        return fund_id
    
    def _save_json(self, fund_data: Dict):
        """Save fund data as JSON file"""
        fund_name = fund_data.get('fund_name') or 'unknown'
        if isinstance(fund_name, str):
            fund_name = fund_name.replace('/', '_').replace('\\', '_')
        else:
            fund_name = 'unknown'
        filename = f"{self.json_path}/{fund_name}_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fund_data, f, indent=2, ensure_ascii=False)
    
    def get_fund_by_url(self, url: str) -> Optional[Dict]:
        """Retrieve fund data by source URL"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM funds WHERE source_url = ?', (url,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        fund_data = dict(row)
        
        # Get returns
        cursor.execute('SELECT period, return_value FROM returns WHERE fund_id = ?', (row['id'],))
        fund_data['returns'] = {r['period']: r['return_value'] for r in cursor.fetchall()}
        
        # Get holdings
        cursor.execute('SELECT holding_name, allocation, sector FROM holdings WHERE fund_id = ?', (row['id'],))
        fund_data['holdings'] = [dict(h) for h in cursor.fetchall()]
        
        # Get FAQs
        cursor.execute('SELECT question, answer FROM faqs WHERE fund_id = ?', (row['id'],))
        fund_data['faqs'] = [dict(f) for f in cursor.fetchall()]
        
        conn.close()
        return fund_data
    
    def search_funds(self, query: str) -> List[Dict]:
        """Search funds by name"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM funds 
            WHERE fund_name LIKE ?
        ''', (f'%{query}%',))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_all_funds(self) -> List[Dict]:
        """Get all funds"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM funds')
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

