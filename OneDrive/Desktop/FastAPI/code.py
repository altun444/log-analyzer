import os
import hashlib
import datetime
import getpass

# 1. PARAMETRLƏRİN TƏYİNİ
# Monitorinq olunacaq qovluğun yolu (Nümunə olaraq cari qovluq götürülüb)
MONITOR_DIR = "./test_qovlugu"
# Həş dəyərlərinin saxlanılacağı baza faylı
HASH_DATABASE = "fayl_bazasi.txt"
# Giriş loqlarının yazılacağı fayl
LOG_FILE = "tehlukesizlik_loqlari.txt"


# 2. LOGİN (GİRİŞ) AUDİTİ FUNKSİYASI
def log_user_access():
    """Sistemə daxil olan istifadəçini və zamanı qeyd edir."""
    current_user = getpass.getuser()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_message = f"[{current_time}] XƏBƏRDARLIQ: İcra edən istifadəçi: {current_user}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_message)
    print(f"[+] Giriş qeydə alındı: {current_user}")


# 3. FAYL BÜTÖVLÜYÜNÜN YOXLANILMASI (SHA-256)
def calculate_sha256(file_path):
    """Faylın unikal rəqəmsal imzasını (Hash) hesablayır."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Faylı hissə-hissə oxuyuruq (böyük fayllarda donma olmasın deyə)
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None


def scan_and_verify():
    """Faylları skan edir və dəyişiklik olub-olmadığını yoxlayır."""
    if not os.path.exists(MONITOR_DIR):
        os.makedirs(MONITOR_DIR)
        print(f"[-] '{MONITOR_DIR}' qovluğu tapılmadı. Yeni boş qovluq yaradıldı. İçi boşdur.")
        return

    # Mövcud bazanı oxuyuruq
    old_hashes = {}
    if os.path.exists(HASH_DATABASE):
        with open(HASH_DATABASE, "r", encoding="utf-8") as f:
            for line in f:
                if " : " in line:
                    f_path, f_hash = line.strip().split(" : ")
                    old_hashes[f_path] = f_hash

    current_hashes = {}
    changes_detected = False

    # Qovluqdakı faylları skan edirik
    for root, dirs, files in os.walk(MONITOR_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            current_hash = calculate_sha256(full_path)
            current_hashes[full_path] = current_hash

            # Yeni fayl yaradılıb?
            if full_path not in old_hashes:
                print(f"🚨 YENİ FAYL AŞKARLANDI: {full_path}")
                changes_detected = True
            # Faylın tərkibi dəyişdirilib?
            elif old_hashes[full_path] != current_hash:
                print(f"🔥 FAYL DƏYİŞDİRİLİB (TƏHLÜKƏ!): {full_path}")
                changes_detected = True

    # Silinmiş faylları yoxlayırıq
    for old_path in old_hashes:
        if old_path not in current_hashes:
            print(f"🗑️ FAYL SİLİNİB: {old_path}")
            changes_detected = True

    # Yeni həş dəyərlərini bazaya yazırıq (Yeniləyirik)
    with open(HASH_DATABASE, "w", encoding="utf-8") as f:
        for f_path, f_hash in current_hashes.items():
            f.write(f"{f_path} : {f_hash}\n")

    if not changes_detected:
        print("✅ Sistem təmizdir. Heç bir icazəsiz fayl dəyişikliyi tapılmadı.")


# Skripti işə salırıq
if __name__ == "__main__":
    print("--- Təhlükəsizlik Skripti İşə Düşdü ---")
    log_user_access()
    scan_and_verify()