# 🔧 Troubleshooting Railway Deployment

## ❌ Masalah Umum dan Solusi

### 1. Build Failed - "No such file or directory"

**Error:**
```
Error: ENOENT: no such file or directory, open 'package.json'
```

**Solusi:**
✅ Pastikan file `nixpacks.toml` ada di root directory
✅ Isi `nixpacks.toml`:
```toml
[phases.setup]
nixPkgs = ['python39']

[phases.install]
cmds = ['pip install -r requirements.txt']

[start]
cmd = 'gunicorn app:app --bind 0.0.0.0:$PORT'
```

### 2. Build Failed - "Requirements not found"

**Error:**
```
Could not open requirements file: No such file or directory: 'requirements.txt'
```

**Solusi:**
✅ Pastikan `requirements.txt` ada di root directory
✅ Isi requirements.txt:
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
qrcode[pil]==7.4.2
Pillow>=9.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.7
```

### 3. Application Error - "Module not found"

**Error:**
```
ModuleNotFoundError: No module named 'app'
```

**Solusi:**
✅ Pastikan file `app.py` ada di root directory
✅ Cek `Procfile`:
```
web: gunicorn app:app
```

### 4. Database Connection Error

**Error:**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server failed
```

**Solusi:**
✅ Tambah PostgreSQL service di Railway:
1. Dashboard → New Service → Database → PostgreSQL
2. Railway otomatis set `DATABASE_URL`

✅ Cek environment variables:
- `DATABASE_URL` harus ada
- Format: `postgresql://user:pass@host:port/dbname`

### 5. Internal Server Error (500)

**Error:**
```
Internal Server Error
```

**Solusi:**
✅ Cek Railway logs:
1. Dashboard → View Logs
2. Cari error detail

✅ Set environment variables:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

✅ Generate secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### 6. Static Files Not Loading

**Error:**
CSS/JS tidak load, 404 error

**Solusi:**
✅ Pastikan folder `templates/` ada
✅ Cek path di HTML template:
```html
<!-- Gunakan CDN untuk CSS/JS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
```

### 7. QR Code Generation Error

**Error:**
```
ImportError: cannot import name 'Image' from 'PIL'
```

**Solusi:**
✅ Update requirements.txt:
```
Pillow>=9.0.0
qrcode[pil]==7.4.2
```

### 8. Session Not Working

**Error:**
Login tidak tersimpan, selalu redirect ke login

**Solusi:**
✅ Set SECRET_KEY di environment variables:
```
SECRET_KEY=your-very-secret-key-here
```

## 🔍 Debugging Steps

### 1. Cek Logs Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs
```

### 2. Test Lokal Dulu
```bash
# Test dengan environment production
export FLASK_ENV=production
export SECRET_KEY=test-key
python app.py
```

### 3. Cek File Structure
Pastikan struktur file seperti ini:
```
project/
├── app.py
├── requirements.txt
├── Procfile
├── railway.json
├── nixpacks.toml
├── runtime.txt
├── .gitignore
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── guru_dashboard.html
    └── admin_dashboard.html
```

## 🚀 Deploy Ulang

Jika masih error, coba deploy ulang:

### 1. Update Code
```bash
git add .
git commit -m "Fix deployment issues"
git push origin main
```

### 2. Redeploy di Railway
1. Dashboard → Settings → Redeploy

### 3. Reset Database (jika perlu)
1. Dashboard → PostgreSQL service → Settings → Delete
2. Tambah PostgreSQL service baru

## 📋 Checklist Deployment

Sebelum deploy, pastikan:

- [ ] ✅ `app.py` ada dan tidak ada syntax error
- [ ] ✅ `requirements.txt` lengkap dan benar
- [ ] ✅ `Procfile` ada: `web: gunicorn app:app`
- [ ] ✅ `railway.json` ada dan benar
- [ ] ✅ `nixpacks.toml` ada dan benar
- [ ] ✅ Folder `templates/` ada dengan semua HTML
- [ ] ✅ PostgreSQL service sudah ditambah
- [ ] ✅ Environment variables sudah diset
- [ ] ✅ Code sudah di-push ke GitHub

## 🆘 Jika Masih Bermasalah

### 1. Cek Railway Status
- https://status.railway.app

### 2. Railway Community
- https://help.railway.app
- Discord: https://discord.gg/railway

### 3. Alternative Deployment
Jika Railway tidak berhasil, coba platform lain:
- **Render**: https://render.com
- **Heroku**: https://heroku.com
- **Vercel**: https://vercel.com (untuk Flask perlu config khusus)

### 4. Deploy Manual
```bash
# Clone repository
git clone your-repo-url
cd your-project

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url

# Run application
gunicorn app:app --bind 0.0.0.0:5000
```

---

**Semoga berhasil! 🎉**