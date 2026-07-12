# Tugas: Revisi Tampilan (UI/UX) - SecureCrypt

## Konteks
Aplikasi SecureCrypt (Flask + Bootstrap 5) sudah **berfungsi penuh** (login, register, encrypt, decrypt semua sudah jalan). Sekarang fokus **HANYA** memperbaiki tampilan (HTML + CSS), jangan ubah logic backend (`app.py`, folder `crypto/`) sama sekali.

File yang boleh diubah:
- `templates/base.html`
- `templates/index.html`
- `templates/login.html`
- `templates/encrypt.html`
- `templates/decrypt.html`
- `static/css/style.css`
- `static/js/main.js` (kalau perlu animasi/interaksi ringan)

## Arah Desain
- Tema: **modern, clean, minimal** — kesan aplikasi security/tech, bukan web sekolahan/warna-warni
- Palet warna: gelap-terang kontras tinggi, misal dasar putih/abu muda + aksen warna gelap (navy/slate) + satu warna aksen terang (hijau/biru) untuk tombol utama & status sukses
- Font: gunakan Google Fonts (misal `Inter` atau `Poppins`) via CDN, jangan font default browser
- Konsisten di semua halaman: navbar, spacing, ukuran tombol, border-radius, shadow

## Detail Per Halaman

### 1. Navbar (base.html)
- Logo/nama "SecureCrypt" pakai icon (boleh pakai Bootstrap Icons via CDN, contoh ikon gembok/shield)
- Menu Home, Encrypt, Decrypt rapi dengan hover effect halus
- Kondisi login: tampilkan "Welcome, {username}" + tombol Logout (beri warna beda, misal outline merah)
- Responsive: jadi hamburger menu di layar kecil

### 2. Halaman Login/Register
- Card di tengah layar dengan shadow lembut dan border-radius besar (rounded-4 ke atas)
- Background halaman beri sedikit gradasi atau pattern halus (jangan polos putih total)
- Input field dengan icon di dalamnya (icon user untuk username, icon gembok untuk password)
- Tombol submit full-width dengan warna aksen, ada hover effect (transisi warna/scale halus)
- Link "Register here" / "Login here" dibuat jelas tapi tidak terlalu mencolok

### 3. Halaman Encrypt & Decrypt
- Card yang sama gaya dengan login, tapi lebih lebar
- Upload file: ganti input file default jadi **drag-and-drop area** yang stylish (area kotak putus-putus, berubah warna saat drag-over), tetap fallback ke klik untuk buka file browser
- Tampilkan nama file yang dipilih dengan jelas + ukuran file
- Radio button pilihan metode (AES/Fernet) dibuat seperti card kecil yang bisa diklik (bukan radio button polos), dengan highlight saat dipilih
- Tombol utama full-width, warna berbeda antara Encrypt (misal hijau/biru) dan Decrypt (misal oranye/ungu) supaya user gampang bedain halaman mana yang sedang dibuka
- Tambahkan loading state pada tombol saat proses berjalan (spinner + teks "Processing...") memakai JS sederhana di `main.js`

### 4. Flash Messages (alert sukses/error)
- Styling ulang alert Bootstrap default jadi lebih modern (rounded, ada icon sesuai jenis pesan — centang untuk sukses, tanda seru untuk error)
- Posisi tetap di atas card, dengan animasi fade-in halus

### 5. Halaman Home (index.html)
- Landing sederhana setelah login: sapaan singkat + dua tombol besar/card menuju Encrypt dan Decrypt
- Boleh tambahkan ilustrasi/icon besar bertema keamanan (pakai SVG dari Bootstrap Icons atau sejenis, jangan pakai gambar berhak cipta)

## Ketentuan Teknis
- Tetap pakai Bootstrap 5 sebagai basis (jangan ganti framework), custom CSS di `style.css` untuk override/tambahan
- Semua warna, font, spacing didefinisikan pakai CSS variables di `:root` supaya konsisten dan gampang diubah, contoh:
  ```css
  :root {
    --color-primary: #2563eb;
    --color-dark: #0f172a;
    --color-light: #f8fafc;
    --radius-lg: 1rem;
    --font-main: 'Inter', sans-serif;
  }
  ```
- Pastikan tetap **responsive** di mobile (test tampilan di lebar layar kecil, jangan ada elemen kepotong)
- Jangan hapus struktur `{{ url_for(...) }}`, `{% if %}`, `{{ form_action }}`, dan elemen `id`/`name` yang dipakai backend/JS — hanya ubah class, styling, dan struktur visual di sekitarnya

## Definisi Selesai
- [ ] Semua halaman (login, register, home, encrypt, decrypt) memakai gaya visual yang konsisten
- [ ] Tidak ada perubahan pada logic backend maupun nama field form yang dibaca `app.py`
- [ ] Tampilan tetap rapi saat dibuka di layar HP (responsive)
- [ ] Flash message, tombol, dan form tetap berfungsi normal setelah restyle
- [ ] Tidak ada asset gambar berhak cipta — hanya pakai icon dari library open-source (Bootstrap Icons, dsb) atau CSS/SVG buatan sendiri

## Instruksi untuk Agent
Kerjakan satu halaman dulu sampai selesai (mulai dari `base.html` karena jadi acuan navbar & style global), lalu lanjut ke halaman lain satu per satu. Setelah tiap halaman selesai diubah, jangan lupa test dengan menjalankan aplikasi dan cek tidak ada elemen yang rusak fungsinya.
