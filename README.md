# 🏫 Sistem Kontrol Guru - MAN Insan Cendekia Kota Kendari

Aplikasi web untuk monitoring dan kontrol aktivitas guru meliputi:
- ✅ **Absensi dengan Scan Barcode** - Guru scan QR code untuk masuk/keluar
- 📊 **Dashboard Real-time** - Tim akademik monitor kehadiran guru
- 📝 **Jurnal Pembelajaran** - Pencatatan materi dan aktivitas mengajar
- 📋 **Manajemen Tugas** - Kontrol tugas yang diberikan kepada siswa
- 🔔 **Notifikasi Otomatis** - Alert jika guru terlambat atau tidak masuk

## 🚀 Cara Instalasi

### 1. Persiapan
```bash
# Clone atau download project ini
# Pastikan Python 3.7+ sudah terinstall
python --version
```

### 2. Install Dependencies
```bash
# Install package yang diperlukan
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
# Jalankan server
python run.py
```

### 4. Akses Aplikasi
- **Komputer**: http://localhost:5000
- **HP/Tablet**: http://[IP-KOMPUTER]:5000
- Contoh: http://192.168.1.100:5000

## 👥 Akun Default

### Admin (Tim Akademik)
- **NIP**: `admin123`
- **Password**: `admin123`

### Guru (Contoh)
- **NIP**: `196801011990031001` (Dr. Ahmad Hidayat)
- **Password**: `guru123`

*Semua guru contoh menggunakan password: `guru123`*

## 📱 Cara Penggunaan

### Untuk Guru:
1. **Login** dengan NIP dan password
2. **Generate QR Code** di dashboard guru
3. **Scan Barcode** untuk absensi masuk/keluar
4. **Isi Jurnal** pembelajaran setelah mengajar
5. **Buat Tugas** untuk siswa

### Untuk Tim Akademik:
1. **Login** sebagai admin
2. **Monitor kehadiran** guru real-time
3. **Tambah guru baru** ke sistem
4. **Lihat laporan** jurnal dan tugas
5. **Kelola jadwal** mengajar

## 🔧 Fitur Utama

### 📊 Dashboard Admin
- Statistik kehadiran real-time
- Monitoring guru yang sedang mengajar
- Alert guru yang terlambat/tidak masuk
- Laporan bulanan kehadiran

### 👨‍🏫 Dashboard Guru
- Status kehadiran hari ini
- QR Code personal untuk absensi
- Form jurnal pembelajaran
- Manajemen tugas siswa

### 📱 Scan Barcode
- Menggunakan kamera HP
- Deteksi QR code otomatis
- Absensi masuk dan keluar
- Notifikasi real-time

### 🔔 Sistem Notifikasi
- Alert jika guru belum masuk saat jadwal mengajar
- Notifikasi tugas yang belum diselesaikan
- Reminder pengisian jurnal

## 🗄️ Database

Aplikasi menggunakan SQLite dengan tabel:
- **Guru** - Data guru dan akun login
- **JadwalMengajar** - Jadwal mengajar per guru
- **Kehadiran** - Record absensi harian
- **JurnalPembelajaran** - Catatan mengajar
- **Tugas** - Tugas yang diberikan siswa

## 🌐 Akses dari HP

### Cara Cek IP Komputer:
**Windows:**
```cmd
ipconfig
```

**Linux/Mac:**
```bash
ifconfig
```

### Setting Firewall:
Pastikan port 5000 tidak diblokir firewall agar HP bisa akses.

## 🔒 Keamanan

- Password di-hash menggunakan Werkzeug
- Session management untuk login
- Role-based access (Admin vs Guru)
- Validasi input untuk mencegah SQL injection

## 📞 Support

Untuk bantuan teknis atau customization:
- Email: [email-support]
- WhatsApp: [nomor-wa]

## 📝 Catatan Pengembangan

### Fitur yang Bisa Ditambahkan:
- [ ] Export laporan ke Excel/PDF
- [ ] Integrasi dengan WhatsApp untuk notifikasi
- [ ] Backup database otomatis
- [ ] Multi-sekolah support
- [ ] Mobile app Android/iOS

### Customization:
- Ubah logo sekolah di `templates/base.html`
- Sesuaikan mata pelajaran di form
- Tambah kelas sesuai kebutuhan
- Modifikasi tampilan dengan CSS

---

**Dibuat untuk MAN Insan Cendekia Kota Kendari** 🏫
*Sistem ini membantu digitalisasi manajemen guru untuk meningkatkan kualitas pendidikan*