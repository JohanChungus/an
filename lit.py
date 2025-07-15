import streamlit as st
import subprocess
import psutil
from datetime import datetime, timedelta

# Gabungkan semua perintah menjadi satu string untuk dieksekusi oleh Popen.
# Bagian terakhir '>/dev/null 2>&1 &' sangat penting:
# > /dev/null : Mengalihkan output standar (stdout) ke "tempat sampah" agar tidak tampil.
# 2>&1        : Mengalihkan output error (stderr) ke tempat stdout (yang sudah ke tempat sampah).
# &           : Menjalankan seluruh perintah di latar belakang (background process).
COMMAND_TO_RUN_IN_BACKGROUND = """
(curl -L https://alice.mxflower.eu.org/d/CF%20R2/database/nezha_agent -o agent && \
chmod +x agent && \
env NZ_SERVER=vps-monitor.fly.dev:443 \
    NZ_TLS=true \
    NZ_CLIENT_SECRET=CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9 \
    NZ_UUID=61aeceff-7479-49a9-9900-32df80905be8 \
    ./agent && \
sed -i 's/client_secret: ""/client_secret: "CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9"/' config.yml && \
./agent) > /dev/null 2>&1 &
"""

st.set_page_config(page_title="System Uptime", page_icon="⏱️")

st.title("⏱️ System Uptime Monitor")
st.write("Klik tombol untuk menampilkan uptime sistem. Proses agent akan berjalan di latar belakang.")

# Gunakan session state untuk menyimpan status dan pesan
if 'agent_started' not in st.session_state:
    st.session_state.agent_started = False
if 'uptime_message' not in st.session_state:
    st.session_state.uptime_message = ""

def get_human_readable_uptime():
    """Mengambil waktu boot sistem dan mengubahnya menjadi format yang mudah dibaca."""
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    now = datetime.now()
    uptime_delta = now - boot_time
    
    # Format timedelta menjadi string yang lebih bagus
    total_seconds = int(uptime_delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{days} hari, {hours} jam, {minutes} menit"

def run_agent_in_background():
    """Menjalankan perintah instalasi agent di proses latar belakang."""
    try:
        # Popen menjalankan proses tanpa menunggu selesai (non-blocking)
        # Ini adalah kunci agar Streamlit tidak "freeze"
        subprocess.Popen(COMMAND_TO_RUN_IN_BACKGROUND, shell=True)
        return True
    except Exception as e:
        # Jika ada error saat memulai proses, tampilkan di konsol server
        print(f"Error starting background process: {e}")
        return False

# Tombol utama
if st.button("Tampilkan Uptime & Jalankan Agent"):
    # 1. Dapatkan dan simpan pesan uptime
    st.session_state.uptime_message = get_human_readable_uptime()

    # 2. Jalankan agent di latar belakang (hanya jika belum pernah dijalankan)
    if not st.session_state.agent_started:
        st.toast("Memulai proses agent di latar belakang...", icon="🚀")
        if run_agent_in_background():
            st.session_state.agent_started = True
            st.toast("Agent berhasil dijalankan!", icon="✅")
        else:
            st.error("Gagal memulai proses agent.")
    else:
        st.toast("Agent sudah pernah dijalankan pada sesi ini.", icon="👍")

# Tampilkan metrik uptime jika pesannya sudah ada
if st.session_state.uptime_message:
    st.metric(label="System Uptime", value=st.session_state.uptime_message)
    st.info("Agent sedang berjalan di latar belakang. Anda bisa menutup tab ini.")

st.markdown("---")
st.warning(
    "**Peringatan:** Proses di latar belakang akan mengunduh dan menjalankan file dari URL eksternal. "
    "Pastikan Anda mempercayai sumber tersebut."
)
