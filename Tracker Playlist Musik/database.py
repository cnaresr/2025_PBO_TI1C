import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_db_connection() -> sqlite3.Connection | None:
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Gagal koneksi DB: {e}")
        return None

def execute_query(query: str, params: tuple = None):
    conn = get_db_connection()
    if not conn:
        return None
    last_id = None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Query gagal: {e}\nQuery: {query[:60]}")
        conn.rollback()
        return None
    finally:
        conn.close()

def fetch_query(query: str, params: tuple = None, fetch_all: bool = True):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall() if fetch_all else cursor.fetchone()
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Fetch gagal: {e}\nQuery: {query[:60]}")
        return None
    finally:
        conn.close()

def get_dataframe(query: str, params: tuple = None) -> pd.DataFrame:
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"ERROR [database.py] Gagal baca DataFrame: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def setup_database_initial():
    print(f"🔍 Memeriksa/membuat tabel 'lagu' di DB: {DB_PATH}")
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS lagu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            artis TEXT,
            genre TEXT,
            durasi INTEGER NOT NULL CHECK(durasi > 0),
            nama_playlist TEXT NOT NULL,
            tanggal_ditambahkan DATE NOT NULL
        );"""
        cursor.execute(sql_create_table)
        conn.commit()
        print("✅ Tabel 'lagu' siap.")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error saat setup tabel: {e}")
        return False
    finally:
        conn.close()

def delete_lagu_by_id(id_lagu: int) -> bool:
    sql = "DELETE FROM lagu WHERE id = ?"
    try: 
        result = execute_query(sql, (id_lagu,))
        return result is not None
    except Exception as e:
        print(f" Error saat hapus lagu: {e}")
        return False
    
def update_lagu_by_id(id_lagu: int, data: dict) -> bool:
    sql = """
    UPDATE lagu
    SET judul = ?, artis = ?, genre = ?, durasi = ?, nama_playlist = ?, tanggal_ditambahkan = ?
    WHERE id = ?
    """
    params = (
        data["judul"],
        data["artis"],
        data["genre"],
        data["durasi"],
        data["nama_playlist"],
        data["tanggal_ditambahkan"],
        id_lagu
    )
    try:
        result = execute_query(sql, params)
        return result is not None
    except Exception as e:
        print(f" Gagal update lagu ID {id_lagu}: {e}")
        return False