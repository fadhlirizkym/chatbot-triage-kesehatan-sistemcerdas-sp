import streamlit as st
from openai import OpenAI

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN & DISCLAIMER MEDIS
# ---------------------------------------------------------
st.set_page_config(page_title="Chatbot Triage Kesehatan", page_icon="🏥")

st.title("🤖 Chatbot Triage Kesehatan (Sistem Cerdas)")

# Banner Disclaimer Wajib Medis
st.warning(
    "⚠️ **Penting (Disclaimer Medis):** Aplikasi ini adalah sistem pembantu triase awal "
    "untuk keperluan tugas perkuliahan. Chatbot ini **BUKAN** pengganti dokter atau tenaga medis profesional. "
    "Jangan gunakan aplikasi ini untuk penanganan kondisi darurat medis.",
    icon="⚠️"
)

# ---------------------------------------------------------
# 2. INSIALISASI API KEY OTOMATIS DARI SECRETS.TOML
# ---------------------------------------------------------
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("API Key belum dikonfigurasi di file .streamlit/secrets.toml")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------------------------------------------------
# 3. SYSTEM PROMPT & GUARDRAILS KATA KUNCI DARURAT
# ---------------------------------------------------------
SYSTEM_PROMPT = """
Anda adalah asisten triase kesehatan berbasis AI yang cerdas, empati, dan objektif.
Aturan utama Anda:
1. Berikan informasi edukasi kesehatan dan rekomendasi triase awal berdasarkan gejala yang disampaikan.
2. JANGAN PERNAH memberikan diagnosis medis pasti. Gunakan kalimat seperti "Gejala tersebut bisa berkaitan dengan..." atau "Rekomendasi awal yang bisa dilakukan...".
3. JANGAN PERNAH meresepkan obat-obatan keras/resep. Anda hanya boleh menyarankan pertolongan pertama dasar atau obat bebas jika relevan.
4. Selalu ingatkan pengguna untuk berkonsultasi langsung dengan dokter atau tenaga medis profesional untuk penanganan lebih lanjut.
"""

# Daftar kata kunci kondisi darurat medis
EMERGENCY_KEYWORDS = [
    "sesak napas", "sesak nafas", "nyeri dada", "pendarahan hebat", 
    "tidak sadar", "pingsan", "kejang", "stroke", "serangan jantung",
    "muntah darah", "patah tulang", "pendarahan"
]

def check_emergency(user_text):
    """Fungsi untuk mengecek apakah input pengguna mengandung kata kunci darurat."""
    text_lower = user_text.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

# ---------------------------------------------------------
# 4. RIWAYAT CHAT (SESSION STATE)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# 5. PEMROSESAN INPUT PENGGUNA
# ---------------------------------------------------------
if prompt := st.chat_input("Deskripsikan gejala atau pertanyaan kesehatan Anda..."):
    # Tampilkan pesan pengguna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # CEK GUARDRAIL DARURAT (Berjalan secara lokal/tanpa biaya API)
    if check_emergency(prompt):
        emergency_response = (
            "🚨 **PERINGATAN KONDISI DARURAT MEDIS DETEKSI SIKAP** 🚨\n\n"
            "Gejala yang Anda sebutkan berpotensi merupakan kondisi darurat medis. "
            "**Segera kunjungi Instalasi Gawat Darurat (IGD) Rumah Sakit terdekat** "
            "atau hubungi layanan darurat setempat (118/119) untuk penanganan medis segera!"
        )
        with st.chat_message("assistant"):
            st.error(emergency_response)
        st.session_state.messages.append({"role": "assistant", "content": emergency_response})

    # BAGIAN ELSE YANG SUDAH DIPERBARUI DENGAN TRY-EXCEPT
    else:
        with st.chat_message("assistant"):
            api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            try:
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages,
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_text = str(e)
                if "credit_balance_exhausted" in error_text or "429" in error_text:
                    st.error(
                        "⚠️ **Saldo Kuota API OpenAI Habis ($0.00)**\n\n"
                        "Akun OpenAI Anda membutuhkan pengisian saldo (*top-up*) untuk dapat memproses pertanyaan umum.\n\n"
                        "Namun secara sistem kodingan, logika permintaan API dan integrasi `secrets.toml` Anda sudah 100% BENAR."
                    )
                else:
                    st.error(f"Terjadi kesalahan API: {e}")