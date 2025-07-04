# model.py
import datetime

class Lagu:
    """
    Representasi satu lagu dalam playlist musik.
    """
    def __init__(self, judul: str, artis: str, genre: str, durasi: int,
                 nama_playlist: str, tanggal_ditambahkan: datetime.date | str, id_lagu: int | None = None):
        self.id = id_lagu
        self.judul = judul.strip() if judul else "Tanpa Judul"
        self.artis = artis.strip() if artis else "Unknown"
        self.genre = genre.strip() if genre else "Lainnya"
        self.durasi = durasi if isinstance(durasi, int) and durasi > 0 else 0
        if not (isinstance(durasi, int) and durasi > 0):
            print(f"Peringatan: Durasi '{durasi}' tidak valid atau nol. Disetel ke 0.")
        self.nama_playlist = nama_playlist.strip() if nama_playlist else "Umum"

        if isinstance(tanggal_ditambahkan, datetime.date):
            self.tanggal_ditambahkan = tanggal_ditambahkan
        elif isinstance(tanggal_ditambahkan, str):
            try:
                self.tanggal_ditambahkan = datetime.datetime.strptime(tanggal_ditambahkan, "%Y-%m-%d").date()
            except ValueError:
                self.tanggal_ditambahkan = datetime.date.today()
        else:
            self.tanggal_ditambahkan = datetime.date.today()

    def __repr__(self):
        return f"Lagu(ID:{self.id}, '{self.judul}' oleh {self.artis}, {self.genre}, {self.durasi} detik)"

    def to_dict(self):
        return {
            "judul": self.judul,
            "artis": self.artis,
            "genre": self.genre,
            "durasi": self.durasi,
            "nama_playlist": self.nama_playlist,
            "tanggal_ditambahkan": self.tanggal_ditambahkan.strftime("%Y-%m-%d")
        }
