import re
from datetime import datetime
from database import AlertDatabase

class LogParser:
    def __init__(self):
        self.db = AlertDatabase()
        # Şüpheli pattern'lar tanımla
        self.suspicious_patterns = {
            'sql_injection': [r'(union|select|insert|drop|delete|exec)\s+', r'(\%27|\'|\-\-|\;)'],
            'xss_attack': [r'(<script|javascript:|onload=|onerror=)', r'(alert\(|confirm\(|prompt\()'],
            'path_traversal': [r'(\.\./|\.\.\\)', r'(/etc/passwd|/windows/system32)'],
            'brute_force': [r'(admin|login|password)', r'(401|403|failed)'],
            'suspicious_user_agent': [r'(sqlmap|nikto|nmap|burp|wget|curl)']
        }
    
    def parse_apache_log(self, log_line):
        """Apache log formatını parse et"""
        # Apache Common Log Format pattern
        pattern = r'(\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(.*?)\]\s+"(.*?)"\s+(\d+)\s+(\d+)'
        match = re.match(pattern, log_line)
        
        if match:
            ip = match.group(1)
            timestamp = match.group(2)
            request = match.group(3)
            status_code = match.group(4)
            size = match.group(5)
            
            return {
                'source_ip': ip,
                'timestamp': timestamp,
                'request': request,
                'status_code': int(status_code),
                'size': int(size),
                'raw_log': log_line.strip()
            }
        return None
    
    def analyze_threat_level(self, parsed_log):
        """Log'u analiz et ve tehdit seviyesi belirle"""
        if not parsed_log:
            return None
            
        threats_found = []
        severity = "Low"
        
        request = parsed_log['request'].lower()
        status_code = parsed_log['status_code']
        
        # SQL Injection kontrolü
        for pattern in self.suspicious_patterns['sql_injection']:
            if re.search(pattern, request, re.IGNORECASE):
                threats_found.append("SQL Injection Attempt")
                severity = "Critical"
        
        # XSS kontrolü
        for pattern in self.suspicious_patterns['xss_attack']:
            if re.search(pattern, request, re.IGNORECASE):
                threats_found.append("XSS Attack")
                severity = "High"
        
        # Path Traversal kontrolü
        for pattern in self.suspicious_patterns['path_traversal']:
            if re.search(pattern, request, re.IGNORECASE):
                threats_found.append("Path Traversal")
                severity = "High"
        
        # Brute Force kontrolü
        if status_code in [401, 403] and any(keyword in request for keyword in ['admin', 'login']):
            threats_found.append("Brute Force Attempt")
            severity = "Medium"
        
        # Admin paneli erişim denemeleri
        if '/admin' in request or '/wp-admin' in request:
            threats_found.append("Admin Panel Access")
            if severity == "Low":
                severity = "Medium"
        
        # 404 hataları çok fazlaysa reconnaissance olabilir
        if status_code == 404:
            threats_found.append("Potential Reconnaissance")
            if severity == "Low":
                severity = "Low"
        
        if not threats_found:
            return None
            
        return {
            'alert_type': ', '.join(threats_found),
            'severity': severity,
            'description': f"Suspicious activity detected from {parsed_log['source_ip']}: {', '.join(threats_found)}"
        }
    
    def process_log_file(self, file_path):
        """Log dosyasını işle ve alert'leri veritabanına kaydet"""
        alerts_created = 0
        
        try:
            with open(file_path, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Log'u parse et
                    parsed_log = self.parse_apache_log(line)
                    if not parsed_log:
                        print(f"Satır {line_num} parse edilemedi: {line[:50]}...")
                        continue
                    
                    # Tehdit analizi yap
                    threat_analysis = self.analyze_threat_level(parsed_log)
                    if threat_analysis:
                        # Alert oluştur
                        self.db.add_alert(
                            timestamp=parsed_log['timestamp'],
                            source_ip=parsed_log['source_ip'],
                            dest_ip="Web Server",  # Apache loglarında destination genelde web server
                            alert_type=threat_analysis['alert_type'],
                            severity=threat_analysis['severity'],
                            description=threat_analysis['description'],
                            raw_log=parsed_log['raw_log']
                        )
                        alerts_created += 1
                        print(f"Alert oluşturuldu: {threat_analysis['alert_type']} - {threat_analysis['severity']}")
                
        except FileNotFoundError:
            print(f"Dosya bulunamadı: {file_path}")
        except Exception as e:
            print(f"Hata oluştu: {e}")
        
        return alerts_created
    
    def process_multiple_logs(self):
        """Örnek logları işle"""
        sample_logs = [
            "192.168.1.100 - - [15/Jun/2025:10:15:30 +0000] \"GET /admin/login HTTP/1.1\" 200 1234",
            "10.0.0.50 - - [15/Jun/2025:10:16:45 +0000] \"POST /wp-admin/admin-ajax.php HTTP/1.1\" 404 567", 
            "192.168.1.200 - - [15/Jun/2025:10:17:22 +0000] \"GET /../../../etc/passwd HTTP/1.1\" 403 890",
            "203.0.113.45 - - [15/Jun/2025:10:18:10 +0000] \"GET /index.php?id=1' UNION SELECT * FROM users-- HTTP/1.1\" 200 2345",
            "198.51.100.23 - - [15/Jun/2025:10:19:05 +0000] \"POST /contact.php HTTP/1.1\" 200 445",
            "192.168.1.150 - - [15/Jun/2025:10:20:30 +0000] \"GET /admin/login HTTP/1.1\" 401 234",
            "192.168.1.150 - - [15/Jun/2025:10:21:15 +0000] \"GET /admin/login HTTP/1.1\" 401 234",
            "192.168.1.150 - - [15/Jun/2025:10:22:00 +0000] \"GET /admin/login HTTP/1.1\" 401 234"
        ]
        
        alerts_created = 0
        for log in sample_logs:
            parsed_log = self.parse_apache_log(log)
            if parsed_log:
                threat_analysis = self.analyze_threat_level(parsed_log)
                if threat_analysis:
                    self.db.add_alert(
                        timestamp=parsed_log['timestamp'],
                        source_ip=parsed_log['source_ip'],
                        dest_ip="Web Server",
                        alert_type=threat_analysis['alert_type'],
                        severity=threat_analysis['severity'],
                        description=threat_analysis['description'],
                        raw_log=parsed_log['raw_log']
                    )
                    alerts_created += 1
        
        return alerts_created

# Test için
if __name__ == "__main__":
    parser = LogParser()
    alerts = parser.process_multiple_logs()
    print(f"{alerts} adet alert oluşturuldu!")
    
    # İstatistikleri göster
    stats = parser.db.get_stats()
    print(f"Toplam Alert: {stats['total']}")
    print(f"Critical: {stats['critical']}, High: {stats['high']}, Medium: {stats['medium']}, Low: {stats['low']}")