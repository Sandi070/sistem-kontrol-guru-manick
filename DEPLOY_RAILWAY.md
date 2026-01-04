# 🚀 Panduan Deploy ke Railway

## 📋 Persiapan File

Pastikan file-file berikut ada di repository GitHub Anda:

### ✅ File Wajib untuk Railway:
- `app.py` - Aplikasi Flask utama
- `requirements.txt` - Dependencies Python
- `Procfile` - Konfigurasi proses Railway
- `railway.json` - Konfigurasi Railway
- `nixpacks.toml` - Konfigurasi build
- `templates/` - Folder template HTML

### 📝 Isi File Konfigurasi:

#### 1. `Procfile`
```
web: gunicorn app:app
```

#### 2. `requirements.txt`
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
qrcode[pil]==7.4.2
Pillow>=9.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.7
```

#### 3. `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 4. `nixpacks.toml`
```toml
[phases.setup]
nixPkgs = ['python39']

[phases.install]
cmds = ['pip install -r requirements.txt']

[phases.build]
cmds = ['echo "Build completed"']

[start]
cmd = 'gunicorn app:app --bind 0.0.0.0:$PORT'
```

## 🔧 Langkah Deploy di Railway

### 1. Persiapan Repository
```bash
# Pastikan semua file sudah di commit dan push ke GitHub
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Setup di Railway
1. Login ke [Railway.app](https://railway.app)
2. Klik "New Project"
3. Pilih "Deploy from GitHub repo"
4. Pilih repository Anda
5. Railway akan otomatis detect sebagai Python project

### 3. Tambah Database PostgreSQL
1. Di dashboard project, klik "New Service"
2. Pilih "Database" → "PostgreSQL"
3. Railway akan otomatis create database dan set environment variables

### 4. Set Environment Variables
Di Railway dashboard, tambahkan variables berikut:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key-here`
- `DATABASE_URL` (otomatis dari PostgreSQL service)

### 5. Deploy
1. Railway akan otomatis build dan deploy
2. Tunggu hingga status "Success"
3. Klik "View Logs" untuk monitor proses

## 🔍 Troubleshooting

### ❌ Build Failed
**Solusi:**
1. Cek `requirements.txt` - pastikan semua dependencies valid
2. Pastikan `Procfile` ada dan benar
3. Cek logs untuk error spesifik

### ❌ Database Connection Error
**Solusi:**
1. Pastikan PostgreSQL service sudah running
2. Cek environment variable `DATABASE_URL`
3. Restart deployment

### ❌ Application Error
**Solusi:**
1. Cek logs Railway untuk error detail
2. Pastikan `app.py` tidak ada syntax error
3. Test lokal dulu sebelum deploy

## 📱 Akses Aplikasi

Setelah deploy sukses:
1. Railway akan berikan URL seperti: `https://your-app.railway.app`
2. Akses URL tersebut
3. Login dengan:
   - **Admin**: NIP=`admin123`, Password=`admin123`
   - **Guru**: Password=`guru123`

## 🔒 Keamanan Production

### Environment Variables yang Harus Diset:
```
FLASK_ENV=production
SECRET_KEY=random-secret-key-yang-aman
DATABASE_URL=postgresql://... (otomatis dari Railway)
```

### Generate Secret Key:
```python
import secrets
print(secrets.token_hex(32))
```

## 📊 Monitoring

### Cek Status Aplikasi:
1. Railway Dashboard → View Logs
2. Monitor CPU/Memory usage
3. Cek database connections

### Backup Database:
Railway PostgreSQL otomatis backup, tapi bisa manual backup juga:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login dan backup
railway login
railway db backup
```

## 🚀 Update Aplikasi

Untuk update aplikasi:
1. Push changes ke GitHub
2. Railway otomatis re-deploy
3. Monitor logs untuk memastikan sukses

```bash
git add .
git commit -m "Update aplikasi"
git push origin main
# Railway otomatis deploy
```

## 📞 Support

Jika masih ada masalah:
1. Cek Railway logs untuk error detail
2. Pastikan semua file konfigurasi benar
3. Test aplikasi lokal dulu
4. Cek Railway documentation: https://docs.railway.app

---

**Aplikasi siap digunakan online! 🎉**