// Global variables
let severityChart;
let timelineChart;

// DOM Elements
const elements = {
    criticalCount: document.getElementById('criticalCount'),
    highCount: document.getElementById('highCount'),
    mediumCount: document.getElementById('mediumCount'),
    lowCount: document.getElementById('lowCount'),
    totalCount: document.getElementById('totalCount'),
    alertsTableBody: document.getElementById('alertsTableBody'),
    severityFilter: document.getElementById('severityFilter'),
    limitFilter: document.getElementById('limitFilter'),
    refreshBtn: document.getElementById('refreshBtn'),
    processLogsBtn: document.getElementById('processLogsBtn'),
    clearAlertsBtn: document.getElementById('clearAlertsBtn'),
    applyFiltersBtn: document.getElementById('applyFiltersBtn'),
    statusMessage: document.getElementById('statusMessage'),
    alertModal: document.getElementById('alertModal')
};

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛡️ CyberWatch Dashboard yükleniyor...');
    initializeDashboard();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    elements.refreshBtn.addEventListener('click', refreshDashboard);
    elements.processLogsBtn.addEventListener('click', processLogs);
    elements.clearAlertsBtn.addEventListener('click', clearAlerts);
    elements.applyFiltersBtn.addEventListener('click', applyFilters);
    
    // Severity filter change
    elements.severityFilter.addEventListener('change', applyFilters);
    
    // Modal close
    const closeModal = document.querySelector('.close');
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            elements.alertModal.style.display = 'none';
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === elements.alertModal) {
            elements.alertModal.style.display = 'none';
        }
    });
}

// Initialize dashboard
async function initializeDashboard() {
    showStatusMessage('Dashboard yükleniyor...', 'success');
    
    try {
        await Promise.all([
            loadStats(),
            loadAlerts(),
            loadCharts()
        ]);
        
        showStatusMessage('Dashboard başarıyla yüklendi!', 'success');
        console.log('✅ Dashboard yükleme tamamlandı');
    } catch (error) {
        console.error('❌ Dashboard yükleme hatası:', error);
        showStatusMessage('Dashboard yüklenirken hata oluştu', 'error');
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        // Update stat cards
        elements.criticalCount.textContent = stats.critical || 0;
        elements.highCount.textContent = stats.high || 0;
        elements.mediumCount.textContent = stats.medium || 0;
        elements.lowCount.textContent = stats.low || 0;
        elements.totalCount.textContent = stats.total || 0;
        
        console.log('📊 İstatistikler güncellendi:', stats);
    } catch (error) {
        console.error('📊 İstatistik yükleme hatası:', error);
        showStatusMessage('İstatistikler yüklenemedi', 'error');
    }
}

// Load alerts
async function loadAlerts() {
    try {
        const severity = elements.severityFilter.value;
        const limit = elements.limitFilter.value || 50;
        
        let url = `/api/alerts?limit=${limit}`;
        if (severity) {
            url += `&severity=${severity}`;
        }
        
        const response = await fetch(url);
        const alerts = await response.json();
        
        displayAlerts(alerts);
        console.log(`🚨 ${alerts.length} alert yüklendi`);
    } catch (error) {
        console.error('🚨 Alert yükleme hatası:', error);
        showStatusMessage('Alert\'ler yüklenemedi', 'error');
    }
}

// Display alerts in table
function displayAlerts(alerts) {
    if (!alerts || alerts.length === 0) {
        elements.alertsTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="no-data">Henüz alert bulunmuyor</td>
            </tr>
        `;
        return;
    }
    
    const alertRows = alerts.map(alert => {
        const severityClass = `severity-${alert.severity.toLowerCase()}`;
        const timestamp = new Date(alert.created_at).toLocaleString('tr-TR');
        
        return `
            <tr onclick="showAlertDetails(${alert.id})" style="cursor: pointer;">
                <td>${timestamp}</td>
                <td>${alert.source_ip || 'N/A'}</td>
                <td>${alert.alert_type}</td>
                <td><span class="${severityClass}">${alert.severity}</span></td>
                <td title="${alert.description}">${truncateText(alert.description, 50)}</td>
                <td>${alert.status}</td>
            </tr>
        `;
    }).join('');
    
    elements.alertsTableBody.innerHTML = alertRows;
}

// Show alert details in modal
window.showAlertDetails = function(alertId) {
    // Bu fonksiyon daha sonra geliştirilecek
    console.log('Alert detayları gösteriliyor:', alertId);
    showStatusMessage('Alert detayları yakında eklenecek', 'success');
};

// Load charts
async function loadCharts() {
    try {
        await Promise.all([
            loadSeverityChart(),
            loadTimelineChart()
        ]);
        console.log('📈 Grafikler yüklendi');
    } catch (error) {
        console.error('📈 Grafik yükleme hatası:', error);
    }
}

// Load severity distribution chart
async function loadSeverityChart() {
    try {
        const response = await fetch('/api/severity-distribution');
        const data = await response.json();
        
        const ctx = document.getElementById('severityChart').getContext('2d');
        
        if (severityChart) {
            severityChart.destroy();
        }
        
        severityChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: data.colors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Severity chart yükleme hatası:', error);
    }
}

// Load timeline chart
async function loadTimelineChart() {
    try {
        const response = await fetch('/api/alert-timeline');
        const data = await response.json();
        
        const ctx = document.getElementById('timelineChart').getContext('2d');
        
        if (timelineChart) {
            timelineChart.destroy();
        }
        
        timelineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.hours,
                datasets: [{
                    label: 'Alert Sayısı',
                    data: data.counts,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    } catch (error) {
        console.error('Timeline chart yükleme hatası:', error);
    }
}

// Process sample logs
async function processLogs() {
    elements.processLogsBtn.disabled = true;
    elements.processLogsBtn.textContent = '⏳ İşleniyor...';
    
    try {
        const response = await fetch('/api/process-sample-logs', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatusMessage(result.message, 'success');
            await refreshDashboard();
        } else {
            showStatusMessage(result.error || 'Log işleme hatası', 'error');
        }
    } catch (error) {
        console.error('Log işleme hatası:', error);
        showStatusMessage('Log işleme sırasında hata oluştu', 'error');
    } finally {
        elements.processLogsBtn.disabled = false;
        elements.processLogsBtn.textContent = '📊 Örnek Log İşle';
    }
}

// Clear all alerts
async function clearAlerts() {
    if (!confirm('Tüm alert\'leri silmek istediğinizden emin misiniz?')) {
        return;
    }
    
    elements.clearAlertsBtn.disabled = true;
    elements.clearAlertsBtn.textContent = '⏳ Temizleniyor...';
    
    try {
        const response = await fetch('/api/clear-alerts', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatusMessage(result.message, 'success');
            await refreshDashboard();
        } else {
            showStatusMessage(result.error || 'Temizleme hatası', 'error');
        }
    } catch (error) {
        console.error('Alert temizleme hatası:', error);
        showStatusMessage('Alert temizleme sırasında hata oluştu', 'error');
    } finally {
        elements.clearAlertsBtn.disabled = false;
        elements.clearAlertsBtn.textContent = '🗑️ Temizle';
    }
}

// Apply filters
async function applyFilters() {
    showStatusMessage('Filtreler uygulanıyor...', 'success');
    await loadAlerts();
}

// Refresh dashboard
async function refreshDashboard() {
    console.log('🔄 Dashboard yenileniyor...');
    await initializeDashboard();
}

// Show status message
function showStatusMessage(message, type = 'success') {
    elements.statusMessage.textContent = message;
    elements.statusMessage.className = `status-message ${type} show`;
    
    setTimeout(() => {
        elements.statusMessage.classList.remove('show');
    }, 3000);
}

// Utility function to truncate text
function truncateText(text, maxLength) {
    if (!text) return 'N/A';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Auto refresh every 30 seconds
setInterval(() => {
    console.log('⏱️ Otomatik yenileme...');
    loadStats();
    loadAlerts();
}, 30000);

console.log('🚀 CyberWatch Dashboard JavaScript yüklendi!');