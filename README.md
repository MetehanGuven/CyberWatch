# 🛡️ CyberWatch SOC Dashboard

**SOC (Security Operations Center) Alert Management Dashboard**

Güvenlik operasyon merkezleri için gerçek zamanlı güvenlik olayı izleme ve alert yönetim sistemi.

## 📋 Özellikler

### 🚨 Alert Management
- Gerçek zamanlı güvenlik alert'leri izleme
- Severity seviyelerine göre kategorize etme (Critical, High, Medium, Low)
- Alert filtreleme ve arama
- Detaylı alert görüntüleme

### 📊 Analytics & Reporting
- Gerçek zamanlı dashboard
- Alert severity dağılım grafikleri
- 24 saatlik alert timeline
- İstatistiksel analiz

### 🔍 Threat Detection
- Apache log analizi
- SQL Injection tespiti
- XSS attack detection
- Path Traversal tespiti
- Brute Force attack monitoring
- Admin panel erişim denemeleri

### 🛠️ Technical Features
- RESTful API
- Responsive web interface
- SQLite veritabanı
- Modüler kod yapısı

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Flask 2.3.3
- SQLite3

### Kurulum Adımları

1. **Projeyi klonla/indir**
```bash
git clone <repo-url>
cd cyberwatch
```

2. **Sanal ortam oluştur**
```bash
python3 -m venv cyberwatch_env
source cyberwatch_env/bin/activate  # MacOS/Linux
# cyberwatch_env\Scripts\activate   # Windows
```

3. **Bağımlılıkları yükle**
```bash
pip install -r requirements.txt
```

4. **Veritabanını başlat**
```bash
python database.py
```

5. **Uygulamayı çalıştır**
```bash
python app.py
```

6. **Browser'da aç**
```
http://127.0.0.1:5000
```

## 📁 Proje Yapısı

```
cyberwatch/
├── app.py                 # Ana Flask uygulaması
├── database.py            # Veritabanı yönetimi
├── log_parser.py          # Log analiz motoru
├── requirements.txt       # Python bağımlılıkları
├── templates/
│   └── index.html        # Dashboard HTML şablonu
├── static/
│   ├── style.css         # CSS stilleri
│   └── script.js         # JavaScript kod
├── sample_logs/
│   └── apache_logs.txt   # Örnek log dosyaları
└── README.md             # Bu dosya
```

## 🔧 API Endpoints

### GET Endpoints
- `GET /` - Ana dashboard sayfası
- `GET /api/stats` - Alert istatistikleri
- `GET /api/alerts` - Alert listesi (filtrelenebilir)
- `GET /api/severity-distribution` - Severity dağılımı
- `GET /api/alert-timeline` - 24 saatlik timeline

### POST Endpoints
- `POST /api/process-sample-logs` - Örnek logları işle
- `POST /api/clear-alerts` - Tüm alert'leri temizle

## 🛡️ Güvenlik Kontrolleri

### Desteklenen Tehdit Türleri
1. **SQL Injection**
   - UNION, SELECT, INSERT, DROP komutları
   - SQL meta karakterleri (' -- ; %)

2. **Cross-Site Scripting (XSS)**
   - Script tag'leri
   - JavaScript event handler'lar
   - Alert, confirm, prompt fonksiyonları

3. **Path Traversal**
   - Directory traversal pattern'leri (../)
   - Sistem dosyası erişim denemeleri

4. **Brute Force**
   - Tekrarlanan login denemeleri
   - 401/403 status code'ları

5. **Admin Panel Reconnaissance**
   - /admin, /wp-admin URL'leri
   - Yönetim paneli tarama

## 💻 Kullanım

### Dashboard Özellikleri
1. **Ana İstatistikler**: Toplam ve severity bazlı alert sayıları
2. **Grafikler**: Doughnut chart (severity) ve line chart (timeline)
3. **Filtreleme**: Severity seviyesi ve limit kontrolü
4. **Alert Tablosu**: Detaylı alert listesi

### Butonlar
- **🔄 Yenile**: Dashboard'u manuel yenile
- **📊 Örnek Log İşle**: Test verisi oluştur
- **🗑️ Temizle**: Tüm alert'leri sil

## 🔬 Test Senaryoları

Sistem şu test senaryolarını içerir:
- SQL injection denemeleri
- XSS attack simülasyonu
- Path traversal test'leri
- Brute force login denemeleri
- Admin panel reconnaissance

## 📈 Geliştirme Planı

### Gelecek Özellikler
- [ ] Email alert sistemi
- [ ] Grafana entegrasyonu
- [ ] Multi-log source desteği
- [ ] Machine learning tabanlı anomali tespiti
- [ ] SIEM entegrasyonu
- [ ] Incident response workflow
- [ ] User authentication

## 🛠️ Teknoloji Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Charts**: Chart.js
- **Security**: Log pattern matching, Regex

## 👨‍💻 Geliştirici

Bu proje SOC (Security Operations Center) analyst pozisyonu için portföy projesi olarak geliştirilmiştir.

### Öğrenilen Beceriler
- Log analizi ve parsing
- Güvenlik pattern tespiti
- Web dashboard geliştirme
- RESTful API tasarımı
- Veritabanı yönetimi
- Real-time data visualization

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---
