import streamlit as st
import subprocess

# Perintah shell yang akan dijalankan
# Disimpan dalam variabel agar lebih mudah dibaca
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

st.title("🚀 Nezha Agent Installer")
st.write(
    "Klik tombol di bawah untuk mengunduh, menginstal, dan menjalankan "
    "agent monitoring Nezha di latar belakang."
)

# Gunakan session_state untuk memastikan proses hanya dijalankan sekali per sesi
if 'agent_started' not in st.session_state:
    st.session_state.agent_started = False

def run_agent_process():
    """Fungsi untuk menjalankan perintah di latar belakang."""
    try:
        # Menampilkan pesan bahwa proses sedang dimulai
        with st.spinner("Memulai proses instalasi agent di latar belakang..."):
            # subprocess.Popen digunakan untuk menjalankan proses di latar belakang
            # shell=True diperlukan karena kita menggunakan operator '&&'
            process = subprocess.Popen(
                COMMAND, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
        
        st.success(f"✅ Proses agent berhasil dimulai di latar belakang dengan PID: {process.pid}")
        st.info("Anda bisa menutup tab ini, agent akan tetap berjalan.")
        st.session_state.agent_started = True

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memulai agent:")
        st.code(str(e))

# Tampilkan tombol hanya jika agent belum dijalankan di sesi ini
if not st.session_state.agent_started:
    if st.button("Jalankan Agent Nezha Sekarang"):
        run_agent_process()
else:
    st.success("Agent sudah pernah dijalankan pada sesi ini.")
    st.info("Jika Anda perlu menjalankannya lagi, silakan muat ulang halaman (refresh).")

st.markdown("---")
st.warning(
    "**Peringatan Keamanan:** Kode ini akan mengunduh dan menjalankan skrip dari internet. "
    "Pastikan Anda mempercayai sumber skrip (`raw.githubusercontent.com/nezhahq/scripts`)."
)
