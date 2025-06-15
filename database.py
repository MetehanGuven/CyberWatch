import sqlite3
from datetime import datetime
import os

class AlertDatabase:
    def __init__(self, db_path='alerts.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Veritabanını oluştur ve tabloları hazırla"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Alerts tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT,
                destination_ip TEXT,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                raw_log TEXT,
                status TEXT DEFAULT 'open',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Statistics tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_alerts INTEGER,
                critical_alerts INTEGER,
                high_alerts INTEGER,
                medium_alerts INTEGER,
                low_alerts INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Veritabanı başarıyla oluşturuldu!")
    
    def add_alert(self, timestamp, source_ip, dest_ip, alert_type, severity, description, raw_log):
        """Yeni alert ekle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (timestamp, source_ip, destination_ip, alert_type, severity, description, raw_log)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, source_ip, dest_ip, alert_type, severity, description, raw_log))
        
        conn.commit()
        conn.close()
    
    def get_alerts(self, limit=100, severity_filter=None):
        """Alert'leri getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if severity_filter:
            cursor.execute('''
                SELECT * FROM alerts WHERE severity = ? 
                ORDER BY created_at DESC LIMIT ?
            ''', (severity_filter, limit))
        else:
            cursor.execute('''
                SELECT * FROM alerts 
                ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_stats(self):
        """Dashboard için istatistikleri getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Toplam alert sayıları
        cursor.execute('SELECT COUNT(*) FROM alerts')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE severity = "Critical"')
        critical = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE severity = "High"')
        high = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE severity = "Medium"')
        medium = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE severity = "Low"')
        low = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'critical': critical,
            'high': high,
            'medium': medium,
            'low': low
        }

# Test için
if __name__ == "__main__":
    db = AlertDatabase()
    print("Veritabanı test edildi!")