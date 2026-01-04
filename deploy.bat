@echo off
echo 🔧 Deploying Fixed Application
echo ===============================

echo 📝 Perbaikan yang sudah dilakukan:
echo ✅ Fix Jinja2 moment error
echo ✅ Tambah API daftar guru  
echo ✅ Update JavaScript admin dashboard
echo ✅ Tambah sample data guru
echo ✅ Fix form handlers

REM Add all files
echo 📝 Adding files to Git...
git add .

REM Commit changes
set /p commit_msg="Enter commit message (default: Fix local issues - ready for deployment): "
if "%commit_msg%"=="" set commit_msg=Fix local issues - ready for deployment
echo 💾 Committing changes...
git commit -m "%commit_msg%"

REM Push to GitHub
echo ⬆️ Pushing to GitHub...
git push origin main

echo.
echo ✅ Files pushed successfully!
echo.
echo 🚀 Railway Deployment:
echo 1. Go to Railway dashboard
echo 2. Settings → Redeploy
echo 3. Add PostgreSQL service if not exists
echo 4. Set environment variables:
echo    - FLASK_ENV=production
echo    - SECRET_KEY=your-secret-key
echo.
echo 🧪 Test Lokal:
echo - URL: http://localhost:5000
echo - Admin: admin123 / admin123
echo - Guru: [NIP guru] / guru123
echo.
echo 📖 Read FIX_LOCAL_ISSUES.md for details
echo ===============================

pause