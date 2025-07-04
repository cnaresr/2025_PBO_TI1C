import sqlite3
import os
from konfigurasi import DB_PATH

def setup_database():
    print(f"🔧 Menyiapkan database di: {DB_PATH}")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS playlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            artus TEXT,
            genre TEXT,
            durasi INTEGER NOT NULL CHECK(durasi > 0),
            nama_playlist TEXT NOT NULL,
            tanggal_ditambahkan TEXT NOT NULL
        );
        """
        print("📦 Membuat tabel 'lagu' (jika belum ada)...")
        cursor.execute(sql_create_table)
        conn.commit()
        print("✅ Tabel 'lagu' siap digunakan.")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error SQLite saat setup: {e}")
        return False
    finally: 
        if conn:
            conn.close()
            print("🔌 Koneksi database ditutup.")

if __name__ == "__main__":
    print("=== Setup Database Playlist Musik ===")
    if setup_database():
        print("✅ Setup selesai")
    else:
        print("❌ Setup gagal")