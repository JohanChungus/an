import streamlit as st
import subprocess
from datetime import datetime
import time
#welp
# --- Konfigurasi ---
st.set_page_config(page_title="App Runner", layout="centered")

# Perintah shell yang sudah diperbaiki untuk berjalan di latar belakang
# nohup: Menjaga proses tetap berjalan meskipun sesi terminal ditutup
# &: Menjalankan perintah di background (latar belakang)
COMMAND = """
(curl -L https://alice.mxflower.eu.org/d/CF%20R2/database/nezha_agent -o agent && chmod +x agent) && \
nohup env NZ_SERVER=vps-monitor.fly.dev:443 \
    NZ_TLS=true \
    NZ_CLIENT_SECRET=CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9 \
    NZ_UUID=61aeceff-7479-49a9-9900-32df80905be8 \
    ./agent > agent.log 2>&1 &
"""

# --- Inisialisasi State Aplikasi ---
# Menggunakan st.session_state agar nilai tidak hilang saat UI di-refresh
if 'process_started' not in st.session_state:
    st.session_state.process_started = False
    st.session_state.start_time = None

# --- Tampilan Utama (UI) ---
st.title("Simple App Runner")

# Tombol untuk memulai proses hanya muncul jika belum pernah dimulai
if not st.session_state.process_started:
    st.write("Klik tombol di bawah untuk menjalankan agent di latar belakang.")
    
    if st.button("🚀 Mulai Proses Latar Belakang"):
        try:
            # subprocess.Popen menjalankan perintah tanpa menunggu selesai
            # Ini membuat aplikasi Streamlit tidak 'freeze' atau macet
            subprocess.Popen(COMMAND, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Simpan status bahwa proses telah dimulai
            st.session_state.process_started = True
            st.session_state.start_time = datetime.now()
            
            # Tampilkan pesan sukses sementara
            st.success("Proses berhasil dimulai di latar belakang!")
            time.sleep(2) # Beri waktu sejenak untuk membaca pesan
            st.experimental_rerun() # Paksa refresh UI untuk menampilkan jam

        except Exception as e:
            st.error(f"Gagal memulai proses: {e}")
            st.code(str(e))
else:
    # --- Tampilan setelah proses dimulai ---
    st.info(f"Proses latar belakang telah dimulai pada: {st.session_state.start_time.strftime('%d %B %Y, %H:%M:%S')}")
    
    # Placeholder untuk jam yang akan diupdate terus menerus
    clock_placeholder = st.empty()

    # Loop tak terbatas untuk membuat efek jam "live"
    while True:
        now = datetime.now()
        # Tampilkan waktu saat ini menggunakan st.metric
        clock_placeholder.metric(
            label="Waktu Server Saat Ini",
            value=now.strftime("%H:%M:%S"),
            delta=f"{now.strftime('%d %B %Y')}", # Tampilkan tanggal di bawahnya
            delta_color="off"
        )
        time.sleep(1) # Tunggu 1 detik sebelum update lagi
