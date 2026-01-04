# 🔧 Fix Railway PORT Error

## ❌ Error yang Terjadi:
```
Error: '$PORT' is not a valid port number. 
Attempt #1 failed with service unavailable. 
Continuing to retry for 1m29s
```

## 🛠️ Solusi yang Sudah Diterapkan:

### 1. Updated Dockerfile
- Menggunakan `start.py` script untuk handle PORT dengan benar
- Validasi PORT number sebelum start gunicorn
- Fallback ke port 8000 jika PORT invalid

### 2. Updated Procfile
- Menggunakan `${PORT:-8000}` syntax untuk fallback
- Format yang lebih compatible dengan Railway

### 3. Updated railway.json
- Timeout diperpanjang ke 300 detik
- Healthcheck path ke root "/"

## 🚀 Langkah Deploy Ulang:

### 1. Push Changes
```bash
git add .
git commit -m "Fix PORT environment variable handling"
git push origin main
```

### 2. Railway Dashboard:
1. **Settings** → **Redeploy**
2. **View Logs** untuk monitor proses
3. Pastikan tidak ada error PORT

### 3. Set Environment Variables (PENTING!)
Di Railway dashboard, pastikan ada:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

**JANGAN set PORT manual** - Railway akan set otomatis

## 🔍 Debugging Steps:

### 1. Cek Logs Railway
- Klik "View Logs"
- Cari pesan "Starting application on port XXXX"
- Pastikan port number valid (bukan $PORT literal)

### 2. Cek Environment Variables
- Railway Dashboard → Variables
- Pastikan PORT tidak di-set manual
- Hanya set FLASK_ENV dan SECRET_KEY

### 3. Test Locally
```bash
# Test dengan PORT environment
export PORT=8000
python start.py

# Atau langsung
gunicorn app:app --bind 0.0.0.0:8000
```

## 🆘 Jika Masih Error:

### Alternatif 1: Gunakan Nixpacks
Ganti `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python start.py"
  }
}
```

### Alternatif 2: Render.com
1. Buat account di render.com
2. Connect GitHub
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python start.py`

### Alternatif 3: Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 📋 Checklist Debug:

- [ ] ✅ File `start.py` ada dan executable
- [ ] ✅ `Dockerfile` menggunakan `python start.py`
- [ ] ✅ Tidak ada PORT di environment variables Railway
- [ ] ✅ FLASK_ENV=production sudah di-set
- [ ] ✅ SECRET_KEY sudah di-set
- [ ] ✅ PostgreSQL service sudah ditambah

## 🎯 Expected Behavior:

Setelah fix:
1. **Build** sukses tanpa error
2. **Logs** menunjukkan "Starting application on port XXXX"
3. **Health check** sukses di "/"
4. **Aplikasi** accessible di Railway URL

## 📞 Last Resort:

Jika semua gagal, hapus project Railway dan buat baru:
1. **Delete project** di Railway
2. **Create new project** dari GitHub
3. **Add PostgreSQL** service
4. **Set environment variables**

---

## 🚀 Quick Commands:

```bash
# Push fix
git add .
git commit -m "Fix PORT handling"
git push origin main

# Then redeploy in Railway dashboard
```

**start.py script akan handle PORT dengan benar! 🎯**