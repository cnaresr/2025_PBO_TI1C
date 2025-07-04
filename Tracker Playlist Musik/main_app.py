# main_app.py
import streamlit as st
import datetime
from model import Lagu
from tracker import PlaylistTracker
from konfigurasi import GENRE_MUSIK

def total_detik(jam:int, menit:int, detik:int) -> int:
    return jam * 3600 + menit * 60 + detik

st.set_page_config(page_title="Tracker Playlist Musik", layout="wide")
st.title("🎵 Tracker Playlist Musik")

@st.cache_resource
def get_tracker():
    return PlaylistTracker()

tracker = get_tracker()

menu = st.sidebar.radio("Pilih Menu", ["Tambah Lagu", "Lihat Playlist", "Statistik"])

def format_durasi(detik: int) -> str:
    jam = detik // 3600
    sisa = detik % 3600
    menit = sisa // 60
    detik_sisa = sisa % 60

    bagian = []
    if jam > 0:
        bagian.append(f"{jam} jam")
    if menit > 0:
        bagian.append(f"{menit} menit")
    if detik_sisa > 0 or not bagian:
        bagian.append(f"{detik_sisa} detik")
    
    return ", ".join(bagian)

# === MENU: TAMBAH LAGU ===
if menu == "Tambah Lagu":
    st.header("➕ Tambah Lagu ke Playlist")
    with st.form("form_tambah_lagu", clear_on_submit=True):
        col1, col2 = st.columns([2, 2])
        with col1:
            judul = st.text_input("Judul Lagu")
            artis = st.text_input("Artis")
            genre = st.selectbox("Genre", GENRE_MUSIK, index=0)
        with col2:
            c_jam, c_mnt, c_det = st.columns(3)
            with c_jam:
                jam_in = st.number_input("Jam", min_value=0, step=1, key="jam_add")
            with c_mnt:
                menit_in = st.number_input("Menit", min_value=0, step=1, key="menit_add")
            with c_det:
                detik_in = st.number_input("Detik", min_value=0, step=1, key="detik_add")
            durasi = total_detik(jam_in, menit_in, detik_in)
            nama_playlist = st.text_input("Nama Playlist")
            tanggal = st.date_input("Tanggal Ditambahkan", value=datetime.date.today())

        submitted = st.form_submit_button("Simpan Lagu")
        if submitted:
            if not judul or not nama_playlist or durasi <= 0:
                st.warning("Judul, durasi (≥1 detik), dan nama playlist wajib diisi!")
            else:
                lagu = Lagu(judul, artis, genre, int(durasi), nama_playlist, tanggal)
                playlist = tracker.get_playlist(nama_playlist)
                if playlist.tambah_lagu(lagu):
                    st.success(f"Lagu '{judul}' berhasil ditambahkan ke playlist '{nama_playlist}'")
                    st.rerun()
                else:
                    st.error("Gagal menyimpan lagu.")

# === MENU: LIHAT PLAYLIST ===
elif menu == "Lihat Playlist":
    st.header("📋 Riwayat Lagu dalam Playlist")
    daftar_playlist = tracker.get_semua_playlist()
    if daftar_playlist:
        pilihan = st.selectbox("Pilih Playlist", daftar_playlist)
        df = tracker.get_dataframe_lagu(pilihan)
        if df.empty:
            st.info("Belum ada lagu di playlist ini.")
        else:
            st.subheader(f"Daftar Lagu di Playlist '{pilihan}'")
            for row in df.itertuples():
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    durasi_tampil = format_durasi(row.durasi)
                    st.markdown(f"🎵 **{row.judul}** oleh *{row.artis}* - Genre: `{row.genre}` - Durasi: {durasi_tampil}")
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{row.id}"):
                        st.session_state["edit_id"] = row.id
                with col3:
                    if st.button("❌ Hapus", key=f"hapus_{row.id}"):
                        if tracker.hapus_lagu(row.id):
                            st.success(f"Lagu '{row.judul}' berhasil dihapus.")
                            st.rerun()
                        else:
                            st.error("Gagal menghapus lagu.")

            # === FORM EDIT ===
            if "edit_id" in st.session_state:
                id_edit = st.session_state["edit_id"]
                lagu_row = df[df["id"] == id_edit].iloc[0]
                with st.form("form_edit_lagu"):
                    st.subheader(f"✏️ Edit Lagu: {lagu_row['judul']}")
                    judul_baru = st.text_input("Judul Lagu", value=lagu_row["judul"])
                    artis_baru = st.text_input("Artis", value=lagu_row["artis"])
                    genre_baru = st.selectbox("Genre", GENRE_MUSIK, index=GENRE_MUSIK.index(lagu_row["genre"]) if lagu_row["genre"] in GENRE_MUSIK else 0)
                    
                    dur_awal = int(lagu_row["durasi"])
                    jam_def = dur_awal // 3600
                    mnt_def = (dur_awal % 3600) // 60
                    def_det = dur_awal % 60

                    c_jam, c_mnt, c_det = st.columns(3)
                    with c_jam:
                        jam_edit = st.number_input("Jam", min_value=0, step=1, value = jam_def, key="jam_edit")
                    with c_mnt:
                        menit_edit = st.number_input("Menit", min_value=0, step=1, value = mnt_def, key="mnt_edit")
                    with c_det:
                        detik_edit = st.number_input("Detik", min_value=0, step=1, value = def_det, key="det_edit")
                    
                    durasi_baru = total_detik(jam_edit, menit_edit, detik_edit)

                    playlist_baru = st.text_input("Nama Playlist", value=lagu_row["nama_playlist"])
                    try:
                        tanggal_str = str(lagu_row["tanggal_ditambahkan"])
                        tanggal_obj = datetime.date.fromisoformat(tanggal_str)
                    except Exception:
                        tanggal_obj = datetime.date.today()
                    tanggal_baru = st.date_input("Tanggal Ditambahkan", value=tanggal_obj)

                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        submit_edit = st.form_submit_button("Simpan Perubahan")
                    with col_b:
                        batal_edit = st.form_submit_button("Batalkan Edit")

                    if batal_edit:
                        st.session_state.pop("edit_id")
                        st.rerun()

                    if submit_edit:
                        data_edit = {
                            "judul": judul_baru,
                            "artis": artis_baru,
                            "genre": genre_baru,
                            "durasi": int(durasi_baru),
                            "nama_playlist": playlist_baru,
                            "tanggal_ditambahkan": tanggal_baru.strftime("%Y-%m-%d")
                        }
                        if tracker.edit_lagu(id_edit, data_edit):
                            st.success("Lagu berhasil diperbarui.")
                            st.session_state.pop("edit_id")
                            st.rerun()
                        else:
                            st.error("Gagal update data lagu.")
    else:
        st.info("Belum ada playlist yang dibuat.")

# === MENU: STATISTIK ===
elif menu == "Statistik":
    st.header("📊 Statistik Playlist")
    daftar_playlist = tracker.get_semua_playlist()
    if not daftar_playlist:
        st.info("Belum ada data playlist.")
    else:
        pilihan = st.selectbox("Pilih Playlist", daftar_playlist)
        playlist = tracker.get_playlist(pilihan)
        total_detik = playlist.total_durasi()
        total_menit = total_detik // 60
        genre_favorit = playlist.genre_terbanyak()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Durasi", f"{total_menit} menit")
        with col2:
            st.metric("Genre Dominan", genre_favorit)
