import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Nama file Databas SQLite
NAMA_DB ='playlist_musik.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

GENRE_MUSIK = [
    "Pop", "Rock", "Jazz", "Hip-Hop", "R&B", "EDM", "Klasik", "Metal", "Reggae", "Dangdut", "Lofi", "Lainnya"
]
GENRE_DEFAULT = "Lainnya"