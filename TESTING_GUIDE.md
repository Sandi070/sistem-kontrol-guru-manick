# 🧪 Panduan Testing - Update Fitur MAN IC Kendari

## 📋 Checklist Testing

### ✅ **1. Zona Waktu WITA**

**Test Case:**
- [ ] Login sebagai admin/guru
- [ ] Buat jurnal pembelajaran baru
- [ ] Check timestamp di database/tampilan
- [ ] Verifikasi waktu sesuai WITA (UTC+8)

**Expected Result:**
- Semua waktu tampil dalam zona WITA
- Jam masuk/keluar sesuai waktu Sulawesi Tenggara

---

### ✅ **2. Kelas Diperluas (X-1 s/d XII-5)**

**Test Case:**
- [ ] Buka form tambah jadwal (Admin)
- [ ] Buka form jurnal pembelajaran (Guru)
- [ ] Buka form tugas (Guru)
- [ ] Verifikasi dropdown kelas menampilkan 15 kelas

**Expected Result:**
```
X-1, X-2, X-3, X-4, X-5
XI-1, XI-2, XI-3, XI-4, XI-5
XII-1, XII-2, XII-3, XII-4, XII-5
```

---

### ✅ **3. Absensi Per Kelas**

**Test Case 1: Absen Masuk**
1. [ ] Buka halaman utama (index)
2. [ ] Klik "Mulai Scan"
3. [ ] Pilih kelas: **X-1**
4. [ ] Pilih mata pelajaran: **Matematika**
5. [ ] Scan QR code guru
6. [ ] Verifikasi pesan sukses

**Expected Result:**
```
✅ Selamat datang [Nama Guru]! 
   Absen masuk kelas X-1 (Matematika) berhasil.
```

**Test Case 2: Absen Keluar**
1. [ ] Scan QR code yang sama
2. [ ] Pilih kelas: **X-1** (sama)
3. [ ] Pilih mata pelajaran: **Matematika** (sama)
4. [ ] Scan QR code guru
5. [ ] Verifikasi pesan sukses

**Expected Result:**
```
✅ Sampai jumpa [Nama Guru]! 
   Absen keluar kelas X-1 (Matematika) berhasil.
```

**Test Case 3: Multiple Kelas**
1. [ ] Absen masuk kelas **X-1** - Matematika
2. [ ] Absen masuk kelas **X-2** - Matematika (kelas berbeda)
3. [ ] Absen keluar kelas **X-1** - Matematika
4. [ ] Absen keluar kelas **X-2** - Matematika
5. [ ] Verifikasi semua tercatat terpisah

**Expected Result:**
- Guru bisa absen masuk/keluar berkali-kali
- Setiap kelas tercatat terpisah
- Dashboard guru menampilkan semua kehadiran

---

### ✅ **4. Monitoring Kehadiran (Admin)**

**Test Case:**
1. [ ] Login sebagai admin
2. [ ] Dashboard → "Lihat Kehadiran Hari Ini"
3. [ ] Verifikasi tabel menampilkan:
   - Nama guru & NIP
   - **Kelas** yang diajar
   - **Mata pelajaran**
   - Jam masuk
   - Jam keluar
   - Status
   - Keterangan

**Expected Result:**
```
| Nama Guru | NIP | Kelas | Mata Pelajaran | Jam Masuk | Jam Keluar | Status |
|-----------|-----|-------|----------------|-----------|------------|--------|
| Ahmad     | 123 | X-1   | Matematika     | 07:30     | 09:00      | Hadir  |
| Ahmad     | 123 | X-2   | Matematika     | 09:15     | 10:45      | Hadir  |
```

---

### ✅ **5. Hapus Guru (Admin)**

**Test Case:**
1. [ ] Login sebagai admin
2. [ ] Dashboard → "Daftar Guru"
3. [ ] Pilih guru dummy/test
4. [ ] Klik icon 🗑️ (merah) di kolom Aksi
5. [ ] Konfirmasi hapus
6. [ ] Verifikasi guru terhapus dari daftar

**Expected Result:**
- Guru terhapus dari database
- Semua data terkait (kehadiran, jurnal, tugas, jadwal) ikut terhapus
- Tidak bisa menghapus akun admin

**⚠️ Warning:** Jangan hapus guru yang masih aktif! Gunakan guru dummy untuk testing.

---

### ✅ **6. Edit Password Guru (Admin)**

**Test Case:**
1. [ ] Login sebagai admin
2. [ ] Dashboard → "Daftar Guru"
3. [ ] Pilih guru test
4. [ ] Klik icon 🔑 (kuning) di kolom Aksi
5. [ ] Masukkan password baru: `newpass123`
6. [ ] Logout
7. [ ] Login dengan NIP guru dan password baru
8. [ ] Verifikasi login berhasil

**Expected Result:**
- Password berhasil diubah
- Guru bisa login dengan password baru
- Password minimal 6 karakter

---

### ✅ **7. Print Jurnal Pembelajaran**

**Test Case:**
1. [ ] Login sebagai admin
2. [ ] Dashboard → "Lihat Jurnal Hari Ini"
3. [ ] Klik tombol **"Print Jurnal"** (hijau)
4. [ ] Masukkan tanggal mulai: `2025-01-01`
5. [ ] Masukkan tanggal selesai: `2025-01-31`
6. [ ] Verifikasi jendela print terbuka
7. [ ] Check isi laporan:
   - [ ] Header: MAN Insan Cendekia Kendari
   - [ ] Periode: 2025-01-01 s/d 2025-01-31
   - [ ] Tabel lengkap dengan data jurnal
   - [ ] Total jurnal
   - [ ] Tanda tangan Tim Akademik

**Expected Result:**
- Laporan print-friendly
- Data lengkap dan terformat rapi
- Bisa di-print atau save as PDF

---

### ✅ **8. Dashboard Guru - Kehadiran Per Kelas**

**Test Case:**
1. [ ] Login sebagai guru
2. [ ] Lihat card "Kehadiran Hari Ini"
3. [ ] Verifikasi menampilkan semua kelas yang diabsen
4. [ ] Check warna status:
   - [ ] 🟢 Hijau: Sudah masuk & keluar
   - [ ] 🟡 Kuning: Sudah masuk, belum keluar

**Expected Result:**
```
Kehadiran Hari Ini
------------------
✅ X-1 - Matematika
   Masuk: 07:30 | Keluar: 09:00

⏳ X-2 - Matematika  
   Masuk: 09:15 | Belum keluar
```

---

## 🔍 **Testing Skenario Lengkap**

### **Skenario 1: Guru Mengajar 3 Kelas**

1. **Pagi (07:30):**
   - Scan QR → Pilih X-1, Matematika → Absen masuk
   - Mengajar sampai 09:00
   - Scan QR → Pilih X-1, Matematika → Absen keluar

2. **Jam 2 (09:15):**
   - Scan QR → Pilih X-2, Matematika → Absen masuk
   - Mengajar sampai 10:45
   - Scan QR → Pilih X-2, Matematika → Absen keluar

3. **Siang (13:00):**
   - Scan QR → Pilih XI-1, Matematika → Absen masuk
   - Mengajar sampai 14:30
   - Scan QR → Pilih XI-1, Matematika → Absen keluar

**Verifikasi:**
- [ ] Dashboard guru menampilkan 3 kehadiran terpisah
- [ ] Admin monitoring menampilkan 3 baris untuk guru ini
- [ ] Semua waktu dalam zona WITA

---

### **Skenario 2: Admin Manajemen**

1. **Monitoring:**
   - [ ] Lihat kehadiran real-time semua guru
   - [ ] Filter per kelas
   - [ ] Export/print laporan

2. **Manajemen Guru:**
   - [ ] Tambah guru baru
   - [ ] Edit password guru
   - [ ] Hapus guru (test account)

3. **Laporan:**
   - [ ] Print jurnal periode 1 minggu
   - [ ] Print jurnal periode 1 bulan
   - [ ] Verifikasi data lengkap

---

## 🐛 **Bug Testing**

### **Edge Cases:**

1. **Absen tanpa pilih kelas:**
   - [ ] Scan QR tanpa pilih kelas
   - Expected: Warning "Pilih kelas dan mata pelajaran terlebih dahulu!"

2. **Absen keluar tanpa masuk:**
   - [ ] Scan QR untuk keluar tanpa absen masuk dulu
   - Expected: Error "Anda belum absen masuk untuk kelas ini"

3. **Double absen keluar:**
   - [ ] Absen keluar 2x untuk kelas yang sama
   - Expected: Error "Anda sudah absen keluar untuk kelas X-1 hari ini"

4. **Edit password < 6 karakter:**
   - [ ] Coba edit password dengan 5 karakter
   - Expected: Error "Password minimal 6 karakter!"

5. **Hapus admin:**
   - [ ] Coba hapus akun admin
   - Expected: Error "Tidak dapat menghapus admin"

---

## ✅ **Acceptance Criteria**

Sistem dianggap **PASS** jika:

- [x] Semua waktu menggunakan zona WITA
- [x] 15 kelas tersedia di semua form
- [x] Absensi per kelas berfungsi sempurna
- [x] Monitoring kehadiran menampilkan data per kelas
- [x] Hapus guru berfungsi (dengan proteksi admin)
- [x] Edit password berfungsi (minimal 6 karakter)
- [x] Print jurnal menghasilkan laporan lengkap
- [x] Dashboard guru menampilkan kehadiran per kelas
- [x] Tidak ada error di console browser
- [x] Tidak ada error di Railway logs

---

## 📊 **Performance Testing**

- [ ] Load time halaman < 3 detik
- [ ] QR scan response < 1 detik
- [ ] Print jurnal generate < 5 detik
- [ ] Database query efficient (check Railway metrics)

---

## 🚀 **Deployment Checklist**

Sebelum deploy ke production:

- [ ] Semua test case PASS
- [ ] No critical bugs
- [ ] Database backup dibuat
- [ ] Railway environment variables checked
- [ ] Documentation updated (UPDATE_FITUR_WITA.md)
- [ ] Team informed about new features

---

## 📞 **Reporting Issues**

Jika menemukan bug:

1. **Screenshot** error message
2. **Catat** langkah reproduksi
3. **Check** Railway logs untuk error detail
4. **Report** dengan format:
   ```
   Bug: [Judul singkat]
   Steps: [Langkah reproduksi]
   Expected: [Yang diharapkan]
   Actual: [Yang terjadi]
   Screenshot: [Attach]
   ```

---

**Happy Testing! 🎉**
