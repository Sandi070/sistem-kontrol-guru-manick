# 🔧 Fix Railway "pip: command not found" Error

## ❌ Error yang Terjadi:
```
/bin/bash: line 1: pip: command not found
ERROR: failed to build: failed to solve: process "/bin/bash -ol pipefail -c pip install -r requirements.txt" did not complete successfully: exit code: 127
```

## 🛠️ Solusi 1: Gunakan Dockerfile (RECOMMENDED)

### 1. Ganti railway.json
Ganti isi `railway.json` dengan:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Gunakan Dockerfile yang sudah dibuat
File `Dockerfile` sudah dibuat otomatis dengan konfigurasi yang benar.

### 3. Push ke GitHub dan redeploy
```bash
git add .
git commit -m "Fix Railway deployment with Dockerfile"
git push origin main
```

## 🛠️ Solusi 2: Fix Nixpacks (Alternative)

### 1. Update nixpacks.toml
File sudah diupdate dengan:
```toml
[phases.setup]
nixPkgs = ['python311', 'pip']

[phases.install]
cmds = ['python -m pip install --upgrade pip', 'pip install -r requirements.txt']

[start]
cmd = 'python -m gunicorn app:app --bind 0.0.0.0:$PORT'
```

### 2. Ganti railway.json ke simple
Rename `railway-simple.json` ke `railway.json`:
```bash
# Di terminal/command prompt
copy railway-simple.json railway.json
```

## 🛠️ Solusi 3: Gunakan Requirements Sederhana

Jika masih error, ganti `requirements.txt` dengan `requirements-simple.txt`:
```bash
copy requirements-simple.txt requirements.txt
```

## 🚀 Langkah Deploy Ulang

### 1. Pilih Solusi (Recommended: Dockerfile)
```bash
# Pastikan menggunakan Dockerfile
git add .
git commit -m "Use Dockerfile for Railway deployment"
git push origin main
```

### 2. Di Railway Dashboard:
1. Go to your project
2. Settings → Redeploy
3. Atau delete project dan buat baru

### 3. Monitor Logs:
- Klik "View Logs" untuk melihat proses build
- Pastikan tidak ada error "pip: command not found"

## 🔍 Jika Masih Error

### Coba Platform Lain:

#### 1. Render.com (Recommended Alternative)
```bash
# Buat account di render.com
# Connect GitHub repository
# Pilih "Web Service"
# Build Command: pip install -r requirements.txt
# Start Command: gunicorn app:app
```

#### 2. Heroku
```bash
# Install Heroku CLI
# heroku create your-app-name
# git push heroku main
```

#### 3. PythonAnywhere
- Upload files manual
- Setup virtual environment
- Configure WSGI

## 📋 Checklist Debugging

- [ ] ✅ File `Dockerfile` ada di root directory
- [ ] ✅ `railway.json` menggunakan "DOCKERFILE" builder
- [ ] ✅ `requirements.txt` tidak ada typo
- [ ] ✅ Semua file sudah di-push ke GitHub
- [ ] ✅ Repository public atau Railway punya akses

## 🆘 Last Resort: Manual Setup

Jika semua gagal, setup manual:

### 1. Download Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Deploy Manual
```bash
railway login
railway init
railway up
```

## 📞 Support

- Railway Discord: https://discord.gg/railway
- Railway Docs: https://docs.railway.app
- GitHub Issues: Buat issue di repository Railway

---

## 🎯 Quick Fix Commands

```bash
# Quick fix dengan Dockerfile
git add .
git commit -m "Fix Railway pip error with Dockerfile"
git push origin main

# Lalu redeploy di Railway dashboard
```

**Dockerfile adalah solusi paling reliable untuk masalah ini! 🚀**