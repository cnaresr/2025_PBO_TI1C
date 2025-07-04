# tracker.py
import datetime
from model import Lagu
import database
import pandas as pd

class Playlist:
    def __init__(self, nama_playlist: str):
        self.nama_playlist = nama_playlist.strip() if nama_playlist else "Umum"

    def tambah_lagu(self, lagu: Lagu) -> bool:
        if not isinstance(lagu, Lagu):
            return False
        sql = """
        INSERT INTO lagu (judul, artis, genre, durasi, nama_playlist, tanggal_ditambahkan)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            lagu.judul,
            lagu.artis,
            lagu.genre,
            lagu.durasi,
            self.nama_playlist,
            lagu.tanggal_ditambahkan.strftime("%Y-%m-%d")
        )
        last_id = database.execute_query(sql, params)
        if last_id:
            lagu.id = last_id
            return True
        return False

    def get_daftar_lagu(self) -> list[Lagu]:
        sql = """
        SELECT * FROM lagu WHERE nama_playlist = ?
        ORDER BY tanggal_ditambahkan DESC, id DESC
        """
        rows = database.fetch_query(sql, (self.nama_playlist,), fetch_all=True)
        daftar = []
        if rows:
            for row in rows:
                lagu = Lagu(
                    id_lagu=row["id"],
                    judul=row["judul"],
                    artis=row["artis"],
                    genre=row["genre"],
                    durasi=row["durasi"],
                    nama_playlist=row["nama_playlist"],
                    tanggal_ditambahkan=row["tanggal_ditambahkan"]
                )
                daftar.append(lagu)
        return daftar

    def total_durasi(self) -> int:
        sql = "SELECT SUM(durasi) FROM lagu WHERE nama_playlist = ?"
        result = database.fetch_query(sql, (self.nama_playlist,), fetch_all=False)
        if result and result[0] is not None:
            return int(result[0])
        return 0

    def genre_terbanyak(self) -> str:
        sql = """
        SELECT genre, COUNT(*) as jumlah FROM lagu
        WHERE nama_playlist = ?
        GROUP BY genre ORDER BY jumlah DESC LIMIT 1
        """
        result = database.fetch_query(sql, (self.nama_playlist,), fetch_all=False)
        if result:
            return result["genre"]
        return "-"

class PlaylistTracker:
    def __init__(self):
        database.setup_database_initial()

    def get_semua_playlist(self) -> list[str]:
        sql = "SELECT DISTINCT nama_playlist FROM lagu ORDER BY nama_playlist ASC"
        rows = database.fetch_query(sql)
        return [row["nama_playlist"] for row in rows] if rows else []

    def get_playlist(self, nama_playlist: str) -> Playlist:
        return Playlist(nama_playlist)

    def get_dataframe_lagu(self, nama_playlist: str = None) -> pd.DataFrame:
        sql = "SELECT * FROM lagu"
        params = None
        if nama_playlist:
            sql += " WHERE nama_playlist = ?"
            params = (nama_playlist,)
        sql += " ORDER BY tanggal_ditambahkan DESC, id DESC"
        return database.get_dataframe(sql, params)
    
    def hapus_lagu(self, id_lagu: int) -> bool:
        from database import delete_lagu_by_id
        return delete_lagu_by_id(id_lagu)

    def edit_lagu(self, id_lagu: int, data_baru: dict) -> bool:
        from database import update_lagu_by_id
        return update_lagu_by_id(id_lagu, data_baru)