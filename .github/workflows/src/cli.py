import sys
import json
from src.parser import stream_log_file
from src.analyzer import analyze_logs

def main():
    if len(sys.argv) < 2:
        print("İstifadə qaydası: python -m src.cli <log_faylının_yolu>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"🔄 {file_path} analiz edilir, xahiş olunur gözləyin...\n")

    try:
        log_stream = stream_log_file(file_path)
        report = analyze_logs(log_stream)
        
        # Nəticəni terminalda gözəl formatda çıxarırıq
        print("============ 📊 LOG ANALYZER REPORT ============")
        print(f"Ümumi sorğu sayı: {report['metrics']['total_requests']}")
        print(f"Ötürülən məlumat: {report['metrics']['total_data_mb']} MB")
        print("\n📌 Status Kodları Dağılımı:")
        for status, count in report['metrics']['status_codes'].items():
            print(f"  {status}: {count} dəfə")
            
        print("\n🚨 Təhlükəsizlik Xəbərdarlıqları:")
        if report['security_alerts']['potential_ddos_ips']:
            print(f"  ⚠️ Potensial DDoS IP-ləri: {report['security_alerts']['potential_ddos_ips']}")
        if report['security_alerts']['brute_force_suspects']:
            print(f"  ⚠️ Brute-force şübhəliləri: {report['security_alerts']['brute_force_suspects']}")
        if not report['security_alerts']['potential_ddos_ips'] and not report['security_alerts']['brute_force_suspects']:
            print("  ✅ Şübhəli fəaliyyət aşkarlanmadı.")
        print("=================================================")

    except FileNotFoundError:
        print(f"❌ Xəta: '{file_path}' adlı fayl tapılmadı.")
    except Exception as e:
        print(f"❌ Gözlənilməz xəta baş verdi: {e}")

if __name__ == "__main__":
    main()
