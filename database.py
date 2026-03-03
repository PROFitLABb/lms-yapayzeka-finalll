import sqlite3

# Veritabanı dosya yolunu belirleyelim
DB_PATH = "lms.db"


def get_connection():
    """Veritabanına bağlanır ve sözlük yapısında veri dönmesini sağlar."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Tabloları oluşturur (Uygulama ilk çalıştığında tetiklenir)."""
    conn = get_connection()
    cursor = conn.cursor()

    # Kullanıcılar Tablosu
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'ogrenci'
        )
        """
    )

    # AI Analiz Sonuçları Tablosu (Projenin kalbi)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            original_text TEXT,
            ai_result TEXT,
            provider TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


# --- Veri İşlem Fonksiyonları ---

def create_user(name, email, role="ogrenci"):
    """Yeni bir kullanıcı (öğrenci/eğitmen) kaydeder."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (name, email, role),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # E-posta zaten varsa hata vermez, False döner
        return False


def get_all_users():
    """Tüm kullanıcıları liste olarak döner."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def save_analysis(user_name, text, result, provider):
    """AI analiz sonucunu veritabanına kaydeder."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO feedback_analysis (user_name, original_text, ai_result, provider)
        VALUES (?, ?, ?, ?)
        """,
        (user_name, text, result, provider),
    )
    conn.commit()
    conn.close()


def get_history():
    """Geçmiş analizleri tarih sırasına göre getirir."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback_analysis ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_statistics():
    """Analiz istatistiklerini döner."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Toplam analiz sayısı
    cursor.execute("SELECT COUNT(*) as total FROM feedback_analysis")
    total = cursor.fetchone()["total"]
    
    # Duygu dağılımı (basit keyword analizi)
    cursor.execute("SELECT ai_result FROM feedback_analysis")
    results = cursor.fetchall()
    
    positive = 0
    negative = 0
    neutral = 0
    
    for row in results:
        text = row["ai_result"].lower()
        if "pozitif" in text or "olumlu" in text or "iyi" in text:
            positive += 1
        elif "negatif" in text or "olumsuz" in text or "kötü" in text:
            negative += 1
        else:
            neutral += 1
    
    conn.close()
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }


def search_history(search_term="", start_date=None, end_date=None):
    """Geçmiş analizlerde arama ve filtreleme yapar."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM feedback_analysis WHERE 1=1"
    params = []
    
    if search_term:
        query += " AND (original_text LIKE ? OR ai_result LIKE ? OR user_name LIKE ?)"
        search_pattern = f"%{search_term}%"
        params.extend([search_pattern, search_pattern, search_pattern])
    
    if start_date:
        query += " AND DATE(created_at) >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND DATE(created_at) <= ?"
        params.append(end_date)
    
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


# Dosya doğrudan çalıştırılırsa veritabanını hazırla
if __name__ == "__main__":
    init_db()

