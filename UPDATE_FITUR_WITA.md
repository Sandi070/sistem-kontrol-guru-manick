# 🔄 Update Fitur Sistem - MAN IC Kendari

## ✅ Fitur yang Diperbarui:

### 1. **Zona Waktu WITA (UTC+8)** 🕐
- **Semua waktu** kini menggunakan zona waktu WITA (Waktu Indonesia Tengah)
- **Fungsi helper** untuk mendapatkan waktu WITA:
  - `get_wita_time()` - Waktu lengkap WITA
  - `get_wita_date()` - Tanggal WITA
  - `get_wita_time_only()` - Jam saja WITA
- **Database timestamps** otomatis menggunakan WITA
- **Absensi, jurnal, tugas** semua tercatat dengan waktu WITA

### 2. **Kelas Diperluas** 📚
Kelas sekarang mencakup:
- **Kelas X**: X-1, X-2, X-3, X-4, X-5
- **Kelas XI**: XI-1, XI-2, XI-3, XI-4, XI-5
- **Kelas XII**: XII-1, XII-2, XII-3, XII-4, XII-5

**Total: 15 kelas** tersedia di semua form (jadwal, jurnal, tugas)

### 3. **Absensi Per Kelas** 📝
**Perubahan Besar:**
- ❌ **Sebelumnya**: Guru absen 1x per hari
- ✅ **Sekarang**: Guru absen per kelas yang diajar

**Cara Kerja:**
1. Guru scan QR code
2. **Pilih kelas** dan **mata pelajaran**
3. Absen masuk untuk kelas tersebut
4. Setelah selesai mengajar, scan lagi untuk absen keluar
5. Guru bisa absen masuk/keluar **berkali-kali** untuk kelas berbeda

**Keuntungan:**
- Tracking lebih detail per kelas
- Monitoring jam mengajar lebih akurat
- Laporan kehadiran lebih komprehensif

### 4. **Manajemen Guru (Admin)** 👥

#### **Hapus Guru:**
- Admin dapat menghapus guru dari sistem
- **Otomatis menghapus** semua data terkait:
  - Kehadiran
  - Jurnal pembelajaran
  - Tugas
  - Jadwal mengajar
- **Proteksi**: Tidak bisa menghapus akun admin

#### **Edit Password:**
- Admin dapat mengubah password guru
- **Validasi**: Password minimal 6 karakter
- Guru langsung bisa login dengan password baru

**Cara Menggunakan:**
1. Dashboard Admin → **"Daftar Guru"**
2. Lihat tombol aksi di setiap baris:
   - 🔑 **Edit Password** (kuning)
   - 🗑️ **Hapus Guru** (merah)

### 5. **Print Jurnal Pembelajaran** 🖨️
**Fitur Baru:**
- Admin dapat mencetak laporan jurnal
- **Filter berdasarkan periode** (tanggal mulai - selesai)
- **Format print-friendly** dengan header MAN IC Kendari
- **Data lengkap**: Guru, kelas, materi, kehadiran siswa

**Cara Menggunakan:**
1. Dashboard Admin → **"Lihat Jurnal Hari Ini"**
2. Klik tombol **"Print Jurnal"** (hijau)
3. Masukkan tanggal mulai (YYYY-MM-DD)
4. Masukkan tanggal selesai (YYYY-MM-DD)
5. Jendela print otomatis terbuka
6. Klik Print atau Save as PDF

**Isi Laporan:**
- Header: MAN Insan Cendekia Kendari
- Periode laporan
- Tabel lengkap dengan:
  - No urut
  - Tanggal
  - Guru (nama & NIP)
  - Kelas
  - Mata pelajaran
  - Materi
  - Metode pembelajaran
  - Kehadiran siswa (Hadir/Tidak Hadir)
  - Catatan
- Total jurnal
- Tanda tangan Tim Akademik

### 6. **Monitoring Kehadiran Aktif** 📊
**Sekarang Berfungsi Penuh:**
- Dashboard Admin → **"Lihat Kehadiran Hari Ini"**
- **Tabel real-time** menampilkan:
  - Nama guru & NIP
  - **Kelas** yang diajar
  - **Mata pelajaran**
  - Jam masuk
  - Jam keluar
  - Status kehadiran
  - Keterangan
- **Update otomatis** setiap ada absensi baru

### 7. **Dashboard Guru - Kehadiran Per Kelas** 📱
**Tampilan Baru:**
- Guru melihat **semua kehadiran hari ini**
- **Per kelas** ditampilkan terpisah
- **Status visual**:
  - 🟢 Hijau: Sudah absen masuk & keluar
  - 🟡 Kuning: Sudah masuk, belum keluar
- **Info detail**: Kelas, mata pelajaran, jam masuk/keluar

## 🔧 **Perubahan Teknis:**

### **Dependencies Baru:**
```
pytz==2023.3  # Untuk timezone WITA
```

### **Model Database Updated:**
```python
class Kehadiran(db.Model):
    # ... existing fields ...
    kelas = db.Column(db.String(10), nullable=False)  # BARU
    mata_pelajaran = db.Column(db.String(50), nullable=False)  # BARU
    created_at = db.Column(db.DateTime, default=lambda: get_wita_time())  # UPDATED
```

### **API Endpoints Baru:**
- `DELETE /api/hapus-guru/<guru_id>` - Hapus guru
- `POST /api/edit-password` - Edit password guru
- `GET /api/print-jurnal` - Get data untuk print jurnal

### **API Endpoints Updated:**
- `POST /api/scan` - Sekarang menerima `kelas` dan `mata_pelajaran`
- `GET /api/kehadiran-hari-ini` - Menampilkan kelas dan mata pelajaran

## 📋 **Cara Menggunakan Fitur Baru:**

### **Untuk Admin:**

#### **1. Monitoring Kehadiran:**
```
Dashboard → "Lihat Kehadiran Hari Ini"
- Lihat semua absensi guru hari ini
- Per kelas dan mata pelajaran
- Real-time update
```

#### **2. Manajemen Guru:**
```
Dashboard → "Daftar Guru"
- Edit Password: Klik icon 🔑 → Masukkan password baru
- Hapus Guru: Klik icon 🗑️ → Konfirmasi hapus
```

#### **3. Print Jurnal:**
```
Dashboard → "Lihat Jurnal Hari Ini" → "Print Jurnal"
- Masukkan periode: 2025-01-01 s/d 2025-01-31
- Otomatis generate laporan
- Print atau save PDF
```

### **Untuk Guru:**

#### **1. Absensi Per Kelas:**
```
1. Scan QR code Anda
2. Pilih kelas yang akan diajar (X-1, X-2, dst)
3. Pilih mata pelajaran
4. Klik "Absen Masuk"
5. Setelah selesai mengajar, scan lagi
6. Pilih kelas yang sama
7. Klik "Absen Keluar"
```

#### **2. Lihat Kehadiran:**
```
Dashboard → Lihat card "Kehadiran Hari Ini"
- Semua kelas yang sudah diabsen muncul
- Status masuk/keluar per kelas
- Warna hijau = selesai, kuning = belum keluar
```

## 🎯 **Manfaat Update:**

### **Untuk Tim Akademik:**
- ✅ **Tracking lebih detail** - Tahu guru mengajar kelas mana
- ✅ **Laporan lengkap** - Print jurnal untuk arsip
- ✅ **Manajemen mudah** - Edit password & hapus guru langsung
- ✅ **Waktu akurat** - Semua pakai zona WITA

### **Untuk Guru:**
- ✅ **Absensi fleksibel** - Per kelas, bukan per hari
- ✅ **Tracking jelas** - Lihat semua kelas yang sudah diabsen
- ✅ **Tidak bingung** - Tahu kelas mana yang belum keluar

## 🚀 **Status Deployment:**

Semua fitur sudah diimplementasikan dan siap di-deploy ke Railway:

```bash
# Jalankan deploy.bat untuk push ke Railway
deploy.bat
```

**Setelah deploy:**
1. ✅ Zona waktu otomatis WITA
2. ✅ Database akan update struktur kehadiran
3. ✅ Semua fitur baru langsung aktif
4. ✅ Data lama tetap aman

## ⚠️ **Catatan Penting:**

### **Migrasi Data:**
- **Kehadiran lama** (tanpa kelas) masih tersimpan
- **Kehadiran baru** akan include kelas & mata pelajaran
- Tidak ada data yang hilang

### **Penggunaan:**
- **Admin** harus re-login setelah deploy
- **Guru** harus re-login setelah deploy
- **QR Code** tetap sama, tidak perlu generate ulang

### **Testing:**
1. Test absensi per kelas
2. Test hapus guru (gunakan guru dummy)
3. Test edit password
4. Test print jurnal
5. Verifikasi waktu WITA di semua fitur

---

## 📞 **Support:**

Jika ada masalah setelah update:
1. Check logs di Railway Dashboard
2. Verifikasi database migration berhasil
3. Test dengan akun admin default: `admin123/admin123`
4. Test dengan akun guru sample: `[NIP]/guru123`

**Sistem siap digunakan dengan fitur-fitur baru! 🎉**
