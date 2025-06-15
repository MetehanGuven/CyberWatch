from flask import Flask, render_template, jsonify, request
from database import AlertDatabase
from log_parser import LogParser
import json

app = Flask(__name__)
db = AlertDatabase()
parser = LogParser()

@app.route('/')
def dashboard():
    """Ana dashboard sayfası"""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """Dashboard istatistikleri"""
    stats = db.get_stats()
    return jsonify(stats)

@app.route('/api/alerts')
def get_alerts():
    """Alert listesini getir"""
    limit = request.args.get('limit', 50, type=int)
    severity_filter = request.args.get('severity', None)
    
    alerts = db.get_alerts(limit=limit, severity_filter=severity_filter)
    
    # Alert'leri JSON formatına çevir
    alert_list = []
    for alert in alerts:
        alert_dict = {
            'id': alert[0],
            'timestamp': alert[1],
            'source_ip': alert[2],
            'destination_ip': alert[3],
            'alert_type': alert[4],
            'severity': alert[5],
            'description': alert[6],
            'raw_log': alert[7],
            'status': alert[8],
            'created_at': alert[9]
        }
        alert_list.append(alert_dict)
    
    return jsonify(alert_list)

@app.route('/api/severity-distribution')
def severity_distribution():
    """Severity dağılımını getir (grafik için)"""
    stats = db.get_stats()
    
    distribution = {
        'labels': ['Critical', 'High', 'Medium', 'Low'],
        'data': [stats['critical'], stats['high'], stats['medium'], stats['low']],
        'colors': ['#FF4444', '#FF8800', '#FFAA00', '#00AA00']
    }
    
    return jsonify(distribution)

@app.route('/api/process-sample-logs', methods=['POST'])
def process_sample_logs():
    """Örnek logları işle"""
    try:
        alerts_created = parser.process_multiple_logs()
        return jsonify({
            'success': True,
            'alerts_created': alerts_created,
            'message': f'{alerts_created} adet yeni alert oluşturuldu!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clear-alerts', methods=['POST'])
def clear_alerts():
    """Tüm alert'leri temizle (test için)"""
    try:
        import os
        if os.path.exists('alerts.db'):
            os.remove('alerts.db')
        # Yeni veritabanı oluştur
        global db
        db = AlertDatabase()
        return jsonify({
            'success': True,
            'message': 'Tüm alert\'ler temizlendi!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alert-timeline')
def alert_timeline():
    """Son 24 saatteki alert dağılımı"""
    # Basit implementasyon - gerçek projede tarih filtreleme yapılacak
    alerts = db.get_alerts(limit=100)
    
    timeline_data = {
        'hours': [],
        'counts': []
    }
    
    # Saatlik gruplandırma (basitleştirilmiş)
    for i in range(24):
        timeline_data['hours'].append(f"{i:02d}:00")
        timeline_data['counts'].append(len([a for a in alerts if str(i) in a[1]]))
    
    return jsonify(timeline_data)

if __name__ == '__main__':
    print("🚀 CyberWatch SOC Dashboard başlatılıyor...")
    print("📊 Dashboard: http://127.0.0.1:5000")
    print("🔍 API Endpoints:")
    print("   - /api/stats (İstatistikler)")
    print("   - /api/alerts (Alert listesi)")
    print("   - /api/process-sample-logs (Örnek log işle)")
    print("\n🛡️  SOC Dashboard hazır!")
    
    app.run(debug=True, host='127.0.0.1', port=5000)