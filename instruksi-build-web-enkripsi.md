# Tugas: Buat Web App - Implementasi Sistem Enkripsi File Menggunakan Python

## Deskripsi
Buat aplikasi web untuk enkripsi & dekripsi file, dengan fitur:
- Enkripsi/dekripsi menggunakan **AES**
- Enkripsi/dekripsi menggunakan **Fernet**
- **Password protection** (hash password untuk login)

## Tech Stack
- Backend: Python (Flask)
- Kriptografi: library `cryptography` (untuk AES & Fernet), `bcrypt` (untuk hash password)
- Frontend: HTML, CSS, JS (boleh pakai Bootstrap dari CDN, jangan terlalu ribet)
- Database: SQLite (untuk simpan user & password hash)

## Fitur yang Harus Ada

1. **Login/Register**
   - User daftar dengan username & password
   - Password disimpan dalam bentuk hash (pakai bcrypt), bukan plaintext
   - Harus login dulu sebelum bisa akses fitur enkripsi/dekripsi

2. **Halaman Enkripsi**
   - Upload file
   - Pilih metode: AES atau Fernet
   - Input password (untuk enkripsi file, boleh beda dari password login)
   - Hasil: file terenkripsi bisa didownload

3. **Halaman Dekripsi**
   - Upload file hasil enkripsi
   - Pilih metode yang sama (AES/Fernet)
   - Input password yang sama saat enkripsi
   - Hasil: file kembali ke bentuk asli, bisa didownload
   - Kalau password salah, tampilkan pesan error (jangan crash)

## Struktur Folder (pakai ini sebagai acuan)

```
enkripsi-file-app/
├── app.py
├── requirements.txt
├── crypto/
│   ├── aes_cipher.py       # encrypt_file_aes(), decrypt_file_aes()
│   ├── fernet_cipher.py    # encrypt_file_fernet(), decrypt_file_fernet()
│   └── password_hasher.py  # hash_password(), verify_password()
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── encrypt.html
│   └── decrypt.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── uploads/
├── outputs/
└── README.md
```

## Ketentuan Teknis Penting
- Key AES/Fernet diturunkan dari password user pakai **PBKDF2** (jangan pakai password mentah langsung sebagai key)
- Simpan salt & IV di dalam file hasil enkripsi supaya bisa dipakai lagi saat dekripsi
- Password login **wajib** di-hash pakai bcrypt, jangan MD5/SHA1
- File hasil enkripsi/dekripsi harus identik dengan file asli setelah proses bolak-balik (encrypt → decrypt)
- Hapus file sementara di folder `uploads/` setelah selesai diproses

## Definisi Selesai
- [ ] App bisa dijalankan dengan `python app.py` tanpa error
- [ ] Enkripsi & dekripsi AES berfungsi, file hasil identik dengan aslinya
- [ ] Enkripsi & dekripsi Fernet berfungsi, file hasil identik dengan aslinya
- [ ] Register & login berfungsi, password tersimpan sebagai hash
- [ ] Ada `requirements.txt` lengkap
- [ ] Ada `README.md` cara install & jalankan

## Instruksi untuk Agent
Bangun bertahap: mulai dari modul `crypto/` dulu (test encrypt→decrypt sampai hasilnya sama persis dengan file asli), baru lanjut backend Flask, baru frontend. Setelah selesai, coba jalankan alur lengkap: register → login → upload file → enkripsi → download → upload hasil → dekripsi → bandingkan dengan file asli.
