# 🎨 SecureCrypt UI/UX Revamp Specification

## Project Overview

Aplikasi **SecureCrypt** (Flask + Bootstrap 5) saat ini sudah berfungsi 100% dari sisi fitur:

* Login
* Register
* Encrypt File
* Decrypt File
* Session Authentication
* File Processing

Fokus pekerjaan ini **hanya pada peningkatan UI/UX dan visual design**.

### ⚠️ Important Rules

**DILARANG mengubah:**

* `app.py`
* Folder `crypto/`
* Logic backend
* Route
* Nama field form
* ID element yang digunakan JavaScript
* Template variable Jinja (`{{ ... }}`)
* Struktur kondisi (`{% if %}`, `{% for %}`)

Perubahan hanya boleh dilakukan pada:

```text
templates/base.html
templates/index.html
templates/login.html
templates/register.html
templates/encrypt.html
templates/decrypt.html

static/css/style.css
static/js/main.js
```

---

# 🎯 Design Vision

SecureCrypt harus terlihat seperti:

* Modern SaaS Application
* Cyber Security Dashboard
* Premium Product
* Clean & Professional
* Minimalis namun elegan

### Hindari

❌ Tampilan seperti tugas kampus

❌ Terlalu banyak warna

❌ Shadow berlebihan

❌ Border tajam

❌ Bootstrap default tanpa kustomisasi

---

# 🎨 Design System

## Color Palette

Gunakan CSS Variables:

```css
:root {
    --primary: #2563eb;
    --primary-hover: #1d4ed8;

    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;

    --dark: #0f172a;
    --dark-soft: #1e293b;

    --gray-100: #f8fafc;
    --gray-200: #e2e8f0;
    --gray-500: #64748b;
    --gray-700: #334155;

    --surface: #ffffff;

    --radius: 20px;
    --shadow:
        0 10px 30px rgba(15,23,42,.08);

    --transition:
        all .25s ease;
}
```

---

## Typography

Gunakan Google Fonts:

```html
Inter
```

Fallback:

```css
font-family:
'Inter',
sans-serif;
```

Target:

* Bersih
* Modern
* Mudah dibaca

---

# 🧩 Global Layout

## Background

Seluruh aplikasi menggunakan:

* Soft gradient
* Warna terang
* Sedikit efek glassmorphism ringan

Contoh nuansa:

```text
putih
biru muda
slate muda
```

Bukan:

```text
hitam penuh
gradient mencolok
warna neon
```

---

# 🔐 Navbar Redesign

## Branding

Tambahkan icon:

```html
shield-lock
```

atau

```html
lock-fill
```

dari Bootstrap Icons.

Tampilan:

```text
🛡 SecureCrypt
```

---

## Navigation Items

Menu:

* Home
* Encrypt
* Decrypt

Hover Effect:

* Smooth transition
* Underline animation
* Color transition

---

## User Section

Saat login:

```text
Welcome, username
```

dan tombol:

```text
Logout
```

Dengan style:

* Outline merah
* Hover merah solid

---

## Mobile Experience

Gunakan:

```html
navbar-toggler
```

Bootstrap 5.

Pastikan:

* Tidak overflow
* Tidak ada teks bertabrakan
* Navigation collapse bekerja sempurna

---

# 🔑 Login & Register Page

## Layout

Form harus berada tepat di tengah layar.

Struktur:

```text
[ Background ]
       |
       |
  [ Card ]
```

---

## Authentication Card

Karakteristik:

* Rounded 24px+
* Shadow lembut
* Glass effect ringan
* Max width 450–500px

---

## Input Fields

Tambahkan icon:

Username

```html
person
```

Password

```html
lock
```

di dalam input.

Style:

* Tinggi nyaman
* Border modern
* Focus state biru

---

## Button

Full Width

```text
Login
Register
```

Style:

* Primary color
* Hover lift effect
* Scale kecil saat hover
* Transition halus

---

## Links

Contoh:

```text
Belum punya akun?
Register sekarang
```

dan

```text
Sudah punya akun?
Login sekarang
```

Gunakan styling modern tanpa terlalu mencolok.

---

# 🏠 Home Page Redesign

## Hero Section

Tampilkan:

```text
Welcome Back,
<username>
```

Subtext:

```text
Protect your files using secure encryption technologies.
```

---

## Security Illustration

Gunakan:

* Bootstrap Icons
* SVG icon

Tema:

```text
Shield
Lock
Key
Encryption
```

Tanpa gambar eksternal.

---

## Quick Actions

Buat 2 action card besar:

### Encrypt Files

* Icon besar
* Deskripsi singkat
* Tombol action

### Decrypt Files

* Icon besar
* Deskripsi singkat
* Tombol action

Layout desktop:

```text
[ Encrypt ] [ Decrypt ]
```

Layout mobile:

```text
[ Encrypt ]
[ Decrypt ]
```

---

# 🔒 Encrypt Page

## Layout

Gunakan card yang lebih lebar:

```text
max-width:
800px
```

---

## Drag & Drop Upload Area

Ganti file input standar menjadi:

```text
Drag & Drop Zone
```

Fitur:

* Border dashed
* Hover effect
* Drag-over state
* Click to browse

---

## File Information

Setelah file dipilih tampilkan:

```text
filename.pdf
2.4 MB
```

secara otomatis.

---

## Encryption Method Selector

Jangan gunakan radio default.

Ubah menjadi:

```text
┌─────────────┐
│ AES         │
└─────────────┘

┌─────────────┐
│ Fernet      │
└─────────────┘
```

Saat dipilih:

* Border berubah
* Background berubah
* Shadow muncul

---

## Encrypt Button

Full Width

Style:

```text
Green / Blue
```

Hover:

* Sedikit naik
* Shadow bertambah

---

# 🔓 Decrypt Page

Gunakan desain yang identik dengan Encrypt.

Perbedaan:

Button utama menggunakan:

```text
Orange
atau
Purple
```

agar pengguna langsung tahu sedang berada di halaman decrypt.

---

# ⚡ Loading State

Saat submit form:

Tombol berubah menjadi:

```text
⏳ Processing...
```

dengan Bootstrap Spinner.

Behavior:

```javascript
disable button
show spinner
prevent double click
```

Implementasi di:

```text
static/js/main.js
```

---

# 🚨 Flash Messages Redesign

Ganti Bootstrap Alert standar menjadi:

## Success

Icon:

```html
check-circle-fill
```

Warna:

```text
green
```

---

## Error

Icon:

```html
exclamation-triangle-fill
```

Warna:

```text
red
```

---

## Info

Icon:

```html
info-circle-fill
```

Warna:

```text
blue
```

---

Tambahkan:

```css
fade-in animation
```

saat muncul.

---

# ✨ Micro Interactions

Tambahkan animasi ringan:

## Card Hover

```css
translateY(-4px)
```

---

## Button Hover

```css
scale(1.02)
```

---

## Navigation Hover

Smooth transition.

---

## Drag Zone Hover

Highlight border.

---

# 📱 Responsive Requirements

Harus optimal pada:

## Mobile

```text
320px+
```

## Tablet

```text
768px+
```

## Desktop

```text
1024px+
```

Pastikan:

* Tidak ada horizontal scroll
* Tidak ada elemen terpotong
* Tombol tetap mudah ditekan

---

# ✅ Definition of Done

Project dianggap selesai jika:

* Semua halaman memiliki visual yang konsisten
* Navbar modern dan responsive
* Login/Register terlihat premium
* Encrypt/Decrypt menggunakan drag & drop upload
* Selector AES/Fernet berbentuk card interaktif
* Flash message modern dengan icon
* Loading state bekerja saat submit
* Mobile responsive
* Tidak ada perubahan backend
* Semua fitur lama tetap berjalan normal
* Tidak ada error Jinja Template
* Tidak ada asset berhak cipta
* Seluruh tampilan terasa seperti aplikasi SaaS keamanan modern
