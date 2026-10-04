# 🩺 Chatbot Triage Kesehatan Berbasis LLM

Aplikasi interaktif **Chatbot Triage Kesehatan Dasar** yang dibangun menggunakan **Python**, **Streamlit**, dan **OpenAI API**. Proyek ini dikembangkan untuk memenuhi Tugas Akhir Mata Kuliah **Sistem Cerdas (Semester Pendek)** di **Universitas Bani Saleh**.

---

## 📌 Deskripsi Proyek

Aplikasi ini dirancang sebagai asisten kecerdasan buatan (AI) untuk membantu melakukan evaluasi dan pengelompokan tingkat urgensi kesehatan awal (*triage*) berdasarkan keluhan/gejala yang diinputkan oleh pengguna. 

> ⚠️ **Sanggahan (Disclaimer):**  
> Aplikasi ini BUKAN pengganti diagnosis medis profesional dari dokter. Sistem ini bertujuan untuk memberikan edukasi awal dan memandu langkah pertolongan pertama secara terstruktur.

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3.10+
* **Framework UI:** Streamlit
* **Model AI:** OpenAI API (`gpt-4o-mini` / `gpt-3.5-turbo`)
* **Manajemen Kredensial:** Streamlit Secrets
* **Version Control:** Git & GitHub

---

## 📁 Struktur Repositori

```text
├── .streamlit/
│   └── secrets.toml.example  # Template kredensial API Key (Dummy)
├── .gitignore                # Melindungi kredensial sensitif
├── README.md                 # Dokumentasi proyek
├── app.py                    # Kode utama aplikasi Streamlit
└── requirements.txt          # Daftar pustaka/library Python

Cara Jalankan Aplikasi secara Lokal (How to Run)
Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer Anda:

1. Kloning Repositori
Bash
git clone [https://github.com/USERNAME_ANDA/NAMA_REPO.git](https://github.com/USERNAME_ANDA/NAMA_REPO.git)
cd NAMA_REPO
2. Buat Lingkungan Virtual (Virtual Environment)
Bash
python -m venv .venv
# Aktifkan di Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
3. Instal Dependensi
Bash
pip install -r requirements.txt
4. Konfigurasi API Key OpenAI
Buat folder .streamlit jika belum ada.

Salin secrets.toml.example menjadi secrets.toml:

Bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
Buka file .streamlit/secrets.toml dan isi dengan OpenAI API Key milik Anda:

Ini, TOML
OPENAI_API_KEY = "sk-proj-MASUKKAN_API_KEY_ANDA_DI_SINI"
5. Jalankan Aplikasi Streamlit
Bash
streamlit run app.py
Aplikasi akan terbuka di browser Anda pada alamat http://localhost:8501.
