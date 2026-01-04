# 🔧 Fix Masalah Aplikasi Lokal

## ✅ Masalah yang Sudah Diperbaiki:

### 1. Error Jinja2 "moment is undefined"
**Masalah:** Template menggunakan `moment()` yang tidak tersedia
**Solusi:** 
- Ganti `{{ moment().format('YYYY-MM-DD') }}` dengan `{{ today }}`
- Update route `guru_dashboard` untuk mengirim variable `today`

### 2. Daftar Guru Tidak Muncul
**Masalah:** Tidak ada API untuk mengambil daftar guru
**Solusi:**
- Tambah API `/api/daftar-guru` 
- Update JavaScript `loadDaftarGuru()` untuk fetch data
- Auto-refresh setelah tambah guru baru

### 3. Sample Data Guru
**Masalah:** Tidak ada data guru untuk testing
**Solusi:**
- Update `init_database()` untuk buat sample guru
- Password default: `guru123`

## 🚀 Test Aplikasi Lokal:

### 1. Jalankan Aplikasi
```bash
python app.py
```

### 2. Akses di Browser
- URL: http://localhost:5000
- Login Admin: `admin123` / `admin123`

### 3. Test Fitur Admin:
1. **Dashboard** - Lihat statistik
2. **Tambah Guru** - Form tambah guru baru
3. **Daftar Guru** - Lihat semua guru dengan QR code
4. **Monitor Kehadiran** - Lihat kehadiran hari ini

### 4. Test Fitur Guru:
1. **Login Guru** - Gunakan NIP guru dan password `guru123`
2. **Generate QR Code** - Buat QR code personal
3. **Dashboard Guru** - Lihat status kehadiran
4. **Jurnal & Tugas** - Form input (UI ready)

## 📋 Data Sample yang Tersedia:

### Admin:
- **NIP**: `admin123`
- **Password**: `admin123`

### Guru Sample:
| Nama | NIP | Password | Mata Pelajaran |
|------|-----|----------|----------------|
| Dr. Ahmad Hidayat | 196801011990031001 | guru123 | Matematika |
| Siti Nurhaliza | 197205151998022001 | guru123 | Fisika |
| Muhammad Rizki | 198003102005011002 | guru123 | Kimia |

## 🔍 Fitur yang Berfungsi:

### ✅ Sudah Berfungsi:
- Login admin dan guru
- Dashboard admin dengan statistik
- Tambah guru baru dengan QR code otomatis
- Daftar guru dengan tampilan QR code
- Generate QR code untuk guru
- Form jurnal dan tugas (UI ready)

### 🚧 Perlu Implementasi Lanjutan:
- Submit jurnal pembelajaran (backend)
- Submit tugas (backend) 
- Scan QR code untuk absensi (perlu kamera)
- Laporan kehadiran
- Jadwal mengajar

## 🛠️ Untuk Deploy Railway:

Setelah test lokal sukses, untuk deploy Railway:

### 1. Push Changes
```bash
git add .
git commit -m "Fix local issues - ready for deployment"
git push origin main
```

### 2. Railway Environment Variables
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### 3. Monitor Logs
- Cek logs Railway untuk error
- Pastikan database PostgreSQL running
- Test URL Railway setelah deploy

## 📱 Test QR Code Scanner:

Untuk test scan QR code:
1. **Generate QR Code** di dashboard guru
2. **Screenshot** QR code
3. **Scan** di halaman utama dengan kamera HP
4. **Cek** dashboard admin untuk kehadiran

---

## 🎉 Aplikasi Siap Digunakan!

Semua masalah utama sudah diperbaiki. Aplikasi bisa digunakan untuk:
- Manajemen guru oleh admin
- Login dan dashboard guru
- Generate QR code untuk absensi
- Monitoring kehadiran real-time