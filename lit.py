import streamlit as st
import subprocess

# Perintah shell yang akan dijalankan
COMMAND = """
curl -L https://raw.githubusercontent.com/nezhahq/scripts/main/agent/install.sh -o agent.sh && \
chmod +x agent.sh && \
env NZ_SERVER=vps-monitor.fly.dev:443 \
    NZ_TLS=true \
    NZ_CLIENT_SECRET=CqmryaDkXPUPoRtdGE8NvfGhjEOLu2b9 \
    NZ_UUID=61aeceff-7479-49a9-9900-32df80905be8 \
    ./agent.sh
"""

st.set_page_config(page_title="Nezha Agent Installer", page_icon="🚀")

st.title("🚀 Nezha Agent Installer dengan Log Real-time")
st.write(
    "Klik tombol di bawah untuk menjalankan instalasi agent Nezha. "
    "Log dari proses akan ditampilkan secara langsung di bawah."
)

def run_command_and_stream_output(command):
    """
    Menjalankan perintah shell dan menghasilkan (yield) outputnya baris per baris.
    """
    # Memulai proses
    # - stderr=subprocess.STDOUT: Menggabungkan output error (stderr) ke output standar (stdout)
    # - text=True: Membaca output sebagai teks (string)
    # - bufsize=1: Mode line-buffered, memastikan output dikirim baris per baris
    # - encoding='utf-8': Menentukan encoding untuk menghindari error
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        bufsize=1 
    )

    # Membaca output dari proses baris per baris secara real-time
    for line in iter(process.stdout.readline, ''):
        yield line
    
    # Tunggu hingga proses selesai dan dapatkan kode return
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        # Jika ada error, kirim pesan error
        yield f"\nPROSES GAGAL dengan kode error: {return_code}\n"
    else:
        yield "\nPROSES SELESAI DENGAN SUKSES\n"


# Tombol untuk memulai proses
if st.button("Jalankan Agent dan Tampilkan Log"):
    st.info("ℹ️ Proses dimulai... Log akan muncul di bawah.")

    # Buat expander untuk menampung log agar UI tetap rapi
    with st.expander("Lihat Log Real-time", expanded=True):
        # Gunakan st.empty() sebagai placeholder yang bisa diupdate terus-menerus
        log_placeholder = st.empty()
        full_log = ""
        
        # Panggil fungsi generator untuk mendapatkan log
        log_stream = run_command_and_stream_output(COMMAND)
        
        # Iterasi melalui setiap baris log yang diterima
        for line in log_stream:
            full_log += line
            # Tampilkan log yang terakumulasi di dalam blok kode
            log_placeholder.code(full_log, language="bash")

    # Tampilkan pesan status akhir setelah proses selesai
    if "PROSES GAGAL" in full_log:
        st.error("❌ Proses instalasi agent gagal. Silakan periksa log di atas.")
    else:
        st.success("✅ Proses agent selesai. Agent seharusnya sekarang berjalan di latar belakang.")

st.markdown("---")
st.warning(
    "**Peringatan Keamanan:** Kode ini akan mengunduh dan menjalankan skrip dari internet. "
    "Pastikan Anda mempercayai sumber skrip (`raw.githubusercontent.com/nezhahq/scripts`)."
)
