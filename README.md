# Database Kader HMI — Cabang Ciputat

![CI](https://github.com/abdurrahmanharits/databasehmiciputat/actions/workflows/ci.yml/badge.svg)

Singkat: venv, CSV contoh, dan Streamlit app untuk visualisasi data kader. Sekarang termasuk:
- uploader CSV sementara di-app
- ringkasan status LK (LK1/2/3)
- contoh kolom tambahan: `Tanggal Lahir`, `Kontak`
- GitHub Actions CI dasar

Quick start (Windows PowerShell):

1. Buat virtual environment

   python -m venv .venv

2. Aktifkan environment

   .\.venv\Scripts\Activate

3. Pasang dependensi

   pip install -r requirements.txt

4. Jalankan Streamlit

   streamlit run app.py

Fitur tambahan
- Upload CSV: gunakan tombol di sidebar untuk mengganti dataset sementara
- Filter `Asal Komisariat` sekarang berupa dropdown (pilih satu komisariat atau "Semua")
- Download CSV filtered: tombol tersedia pada app

File penting:
- `data/kaders_hmi_ciputat.csv` — contoh data (termasuk `Tanggal Lahir`, `Kontak`) — nilai `Asal Komisariat` diperbarui ke daftar komisariat standar
- `app.py` — Streamlit visualizer + uploader + ringkasan LK
- `.github/workflows/ci.yml` — CI sederhana yang memeriksa instalasi

Kontribusi
- Mau format field lain atau peta? Beri tahu saya file sumber atau kolom yang ingin ditambahkan.