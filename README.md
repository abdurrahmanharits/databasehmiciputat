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
- Filter `Asal Komisariat` sekarang berupa dropdown (pilih satu komisariat atau "Semua"). Pilihan `Kampus` otomatis dibatasi sesuai mapping komisariat→institusi.
- Upload CSV: app menerapkan **validasi ketat**, tetapi juga **menormalisasi** label komisariat yang sudah ada di database (mis. `Komisariat Ekonomi`) — nama yang tidak dikenal akan ditambahkan ke mapping otomatis berdasarkan nilai `Kampus` yang ada di file sehingga tidak langsung ditolak. Jika kampus tidak sesuai mapping atau ada komisariat benar-benar baru tanpa kampus, app akan menolak upload.
- Semua tabel yang ditampilkan di dashboard sekarang menampilkan kolom nomor (`No`) mulai dari **1** (tidak lagi dari 0).
- Download CSV filtered: tombol tersedia pada app — **file CSV yang diunduh sekarang menyertakan kolom `No` (1-based)**.

File penting:
- `data/kaders_hmi_ciputat.csv` — contoh data (termasuk `Tanggal Lahir`, `Kontak`) — `Kampus` disesuaikan menurut mapping komisariat
- `app.py` — Streamlit visualizer + uploader + ringkasan LK + validasi mapping
- `.github/workflows/ci.yml` — CI sederhana yang memeriksa instalasi

Kontribusi
- Mau format field lain atau peta? Beri tahu saya file sumber atau kolom yang ingin ditambahkan.

Deployment note: pushed a small change to force redeploy — if you host on Streamlit Cloud, open the app's "Manage app" and trigger a redeploy or wait for the new build to finish.