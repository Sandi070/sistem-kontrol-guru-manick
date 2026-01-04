# 📖 Panduan Penggunaan Sistem Kontrol Guru

## 🚀 Cara Menjalankan Aplikasi

### 1. Jalankan Server
```bash
# Opsi 1: Menggunakan file run.py
python run.py

# Opsi 2: Menggunakan file batch (Windows)
start.bat

# Opsi 3: Menggunakan file shell (Linux/Mac)
./start.sh
```

### 2. Akses Aplikasi
- **Komputer**: http://localhost:5000
- **HP/Tablet**: http://10.130.96.119:5000 (sesuaikan dengan IP komputer Anda)

## 👥 Akun Login Default

### Admin (Tim Akademik)
- **NIP**: `admin123`
- **Password**: `admin123`

### Guru Contoh
Semua guru menggunakan password: `guru123`

| Nama | NIP | Mata Pelajaran |
|------|-----|----------------|
| Dr. Ahmad Hidayat, S.Pd., M.Pd. | 196801011990031001 | Matematika |
| Siti Nurhaliza, S.Si., M.Pd. | 197205151998022001 | Fisika |
| Muhammad Rizki, S.Pd., M.Pd. | 198003102005011002 | Kimia |
| Fatimah Azzahra, S.Pd. | 198507202010012003 | Biologi |
| Andi Pratama, S.Pd. | 199001152015031004 | Bahasa Indonesia |

## 📱 Cara Menggunakan Fitur

### Untuk Guru:

#### 1. Login
1. Buka aplikasi di browser
2. Klik "Login Sistem"
3. Masukkan NIP dan password
4. Klik "Login"

#### 2. Generate QR Code
1. Setelah login, masuk ke dashboard guru
2. Klik "Buat QR Code" jika belum ada
3. QR Code akan muncul di dashboard
4. Screenshot atau simpan QR Code untuk absensi

#### 3. Absensi dengan Scan Barcode
1. Di halaman utama, klik "Mulai Scan"
2. Izinkan akses kamera
3. Arahkan kamera ke QR Code guru
4. Sistem akan otomatis mencatat absensi masuk/keluar

#### 4. Isi Jurnal Pembelajaran
1. Di dashboard guru, klik "Buat Jurnal"
2. Isi form:
   - Tanggal
   - Kelas
   - Mata Pelajaran
   - Materi Pembelajaran
   - Metode Pembelajaran
   - Jumlah siswa hadir/tidak hadir
   - Catatan
3. Klik "Simpan Jurnal"

#### 5. Buat Tugas
1. Di dashboard guru, klik "Buat Tugas"
2. Isi form:
   - Judul Tugas
   - Deskripsi Tugas
   - Kelas
   - Mata Pelajaran
   - Tanggal Diberikan
   - Deadline
3. Klik "Simpan Tugas"

### Untuk Tim Akademik (Admin):

#### 1. Login Admin
1. Gunakan NIP: `admin123` dan Password: `admin123`
2. Masuk ke dashboard admin

#### 2. Monitor Kehadiran
1. Di dashboard admin, klik "Lihat Kehadiran Hari Ini"
2. Lihat status kehadiran semua guru
3. Pantau guru yang terlambat atau belum masuk

#### 3. Tambah Guru Baru
1. Klik "Tambah Guru"
2. Isi form data guru:
   - NIP
   - Nama Lengkap
   - Mata Pelajaran
   - Email
   - Password
3. Sistem otomatis generate QR Code untuk guru baru

#### 4. Lihat Laporan
1. Klik menu yang tersedia:
   - Kehadiran Hari Ini
   - Daftar Guru
   - Jurnal Pembelajaran
   - Tugas Aktif

## 🔧 Fitur Utama

### ✅ Absensi Real-time
- Scan QR Code untuk masuk/keluar
- Notifikasi otomatis saat absen
- Tracking waktu masuk dan keluar

### 📊 Dashboard Monitoring
- Statistik kehadiran real-time
- Status guru yang sedang mengajar
- Alert guru yang terlambat

### 📝 Jurnal Pembelajaran
- Pencatatan materi harian
- Tracking kehadiran siswa
- Catatan metode pembelajaran

### 📋 Manajemen Tugas
- Buat dan kelola tugas siswa
- Set deadline tugas
- Monitor status tugas

## 📱 Akses dari HP

### Cara Cek IP Komputer:
1. Buka Command Prompt (Windows)
2. Ketik: `ipconfig`
3. Cari "IPv4 Address" pada koneksi yang aktif
4. Gunakan IP tersebut: `http://[IP]:5000`

Contoh: `http://192.168.1.100:5000`

## ⚠️ Troubleshooting

### Aplikasi Tidak Bisa Diakses dari HP
1. Pastikan HP dan komputer dalam jaringan WiFi yang sama
2. Matikan firewall Windows sementara
3. Cek IP komputer dengan `ipconfig`

### Error saat Install Dependencies
```bash
# Jika ada error Pillow, coba:
pip install --upgrade pip
pip install Flask Flask-SQLAlchemy Werkzeug qrcode[pil]
```

### Database Error
```bash
# Hapus database dan buat ulang:
del man_ic_system.db
python run.py
```

## 📞 Support

Jika ada kendala teknis:
1. Cek log error di terminal
2. Restart aplikasi dengan `Ctrl+C` lalu `python run.py`
3. Pastikan semua dependencies terinstall

---

**Sistem ini siap digunakan untuk MAN Insan Cendekia Kota Kendari** 🏫