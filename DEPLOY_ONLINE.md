# 🌐 Panduan Deploy Online - Sistem Kontrol Guru

## 🚀 Pilihan Platform Hosting Gratis

### 1. **Railway** ⭐ (PALING MUDAH - RECOMMENDED)

**Kelebihan:**
- Setup paling mudah
- Support database PostgreSQL gratis
- Auto-deploy dari GitHub
- Domain gratis (.railway.app)

**Langkah Deploy:**

1. **Persiapan GitHub**
   ```bash
   # Upload project ke GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME/sistem-kontrol-guru.git
   git push -u origin main
   ```

2. **Deploy ke Railway**
   - Buka https://railway.app
   - Login dengan GitHub
   - Klik "New Project" → "Deploy from GitHub repo"
   - Pilih repository Anda
   - Railway akan otomatis detect Flask app
   - Tunggu build selesai (~3-5 menit)

3. **Setup Database (Opsional)**
   - Di dashboard Railway, klik "Add Service" → "Database" → "PostgreSQL"
   - Railway akan otomatis connect ke app

4. **Akses Aplikasi**
   - Klik "View Logs" untuk melihat URL
   - URL format: `https://sistem-kontrol-guru-production.up.railway.app`

---

### 2. **Render** ⭐ (BAGUS UNTUK FLASK)

**Kelebihan:**
- Khusus untuk web apps
- SSL gratis
- Auto-deploy dari GitHub

**Langkah Deploy:**

1. **Upload ke GitHub** (sama seperti Railway)

2. **Deploy ke Render**
   - Buka https://render.com
   - Login dengan GitHub
   - Klik "New" → "Web Service"
   - Connect repository
   - Settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Python Version**: 3.9.16

3. **Akses Aplikasi**
   - URL format: `https://sistem-kontrol-guru.onrender.com`

---

### 3. **Heroku** (KLASIK)

**Kelebihan:**
- Platform paling terkenal
- Dokumentasi lengkap
- Add-ons banyak

**Langkah Deploy:**

1. **Install Heroku CLI**
   - Download dari https://devcenter.heroku.com/articles/heroku-cli

2. **Deploy**
   ```bash
   # Login Heroku
   heroku login
   
   # Buat app
   heroku create sistem-kontrol-guru-manic
   
   # Deploy
   git push heroku main
   
   # Buka app
   heroku open
   ```

---

### 4. **PythonAnywhere** (KHUSUS PYTHON)

**Kelebihan:**
- Khusus Python
- Interface web mudah
- Support Flask langsung

**Langkah Deploy:**

1. **Daftar di PythonAnywhere**
   - Buka https://www.pythonanywhere.com
   - Daftar akun gratis

2. **Upload Files**
   - Gunakan "Files" tab
   - Upload semua file project

3. **Setup Web App**
   - Klik "Web" tab
   - "Add a new web app"
   - Pilih Flask
   - Set path ke `app.py`

---

### 5. **Vercel** (DENGAN ADAPTASI)

**Kelebihan:**
- Deploy super cepat
- CDN global
- Domain custom gratis

**Langkah Deploy:**

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

---

## 🔧 Konfigurasi Khusus untuk Online

### Environment Variables yang Diperlukan:

```bash
# Untuk production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname  # Jika pakai PostgreSQL
PORT=5000  # Untuk Heroku
```

### File yang Sudah Disiapkan:

- ✅ `Procfile` - Untuk Heroku
- ✅ `railway.json` - Untuk Railway
- ✅ `render.yaml` - Untuk Render
- ✅ `vercel.json` - Untuk Vercel
- ✅ `runtime.txt` - Spesifikasi Python version
- ✅ `requirements.txt` - Dependencies (sudah include gunicorn)

---

## 📱 Akses dari HP Setelah Online

Setelah deploy berhasil, aplikasi bisa diakses dari mana saja:

```
https://your-app-name.railway.app
https://your-app-name.onrender.com
https://your-app-name.herokuapp.com
```

**Keuntungan Online:**
- ✅ Akses dari mana saja (tidak perlu WiFi yang sama)
- ✅ Tidak perlu komputer menyala terus
- ✅ SSL/HTTPS otomatis (aman)
- ✅ Backup otomatis
- ✅ Bisa diakses banyak orang bersamaan

---

## 🎯 Rekomendasi Platform

### Untuk Pemula: **Railway** 
- Paling mudah setup
- Auto-detect Flask
- Database gratis

### Untuk Production: **Render**
- Lebih stabil
- Performance bagus
- SSL gratis

### Untuk Eksperimen: **Vercel**
- Deploy paling cepat
- CDN global

---

## 🔍 Troubleshooting

### Error "Application failed to start"
```bash
# Cek logs di platform hosting
# Pastikan gunicorn terinstall
# Cek Procfile sudah benar
```

### Database Error
```bash
# Untuk PostgreSQL online, update connection string
# Pastikan environment variables sudah set
```

### QR Code tidak muncul
```bash
# Pastikan Pillow terinstall
# Cek error di logs platform
```

---

## 📞 Support

Jika ada kendala deploy:
1. Cek logs di platform hosting
2. Pastikan semua file config sudah ada
3. Test dulu di local dengan `gunicorn app:app`

**Aplikasi siap go online! 🚀**