from collections import Counter
from typing import Generator, Dict, List, Tuple

def analyze_logs(log_stream: Generator[Dict, None, None]) -> Dict:
    """Loq axınını analiz edir və hesabat hazırlayır."""
    ip_counter = Counter()
    status_counter = Counter()
    url_counter = Counter()
    total_size = 0
    total_requests = 0
    
    # Anomaliya təyini üçün xüsusi sayğaclar
    failed_login_ips = Counter() # 401 və ya 403 qaytaran IP-lər

    for log in log_stream:
        total_requests += 1
        ip_counter[log['ip']] += 1
        status_counter[log['status']] += 1
        url_counter[log['url']] += 1
        total_size += log['size']

        # Brute-force şübhəsi: Giriş icazəsi olmayan səhifələrə çox müraciət edənlər
        if log['status'] in:
            failed_login_ips[log['ip']] += 1

    # DDoS şübhəsi: Həddindən artıq çox sorğu göndərən IP-lər (Məsələn, ümumi sorğunun 20%-dən çoxu)
    suspicious_ddos = [ip for ip, count in ip_counter.items() if count > (total_requests * 0.2) and total_requests > 100]

    return {
        "metrics": {
            "total_requests": total_requests,
            "total_data_mb": round(total_size / (1024 * 1024), 2),
            "status_codes": dict(status_counter)
        },
        "top_attackers": ip_counter.most_common(5),
        "top_requested_urls": url_counter.most_common(5),
        "security_alerts": {
            "potential_ddos_ips": suspicious_ddos,
            "brute_force_suspects": [ip for ip, count in failed_login_ips.items() if count > 20]
        }
    }
