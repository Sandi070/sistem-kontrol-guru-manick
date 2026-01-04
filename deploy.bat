@echo off
echo 🆕 Deploying New Features - MAN IC Kendari
echo ==========================================

echo 📝 Fitur baru yang ditambahkan:
echo ✅ Monitoring Jurnal Pembelajaran (Admin)
echo ✅ Monitoring Tugas Aktif (Admin)
echo ✅ Submit Jurnal Pembelajaran (Guru)
echo ✅ Submit Tugas (Guru)
echo ✅ Update Mata Pelajaran MAN IC
echo ✅ Sample data guru mata pelajaran agama

REM Add all files
echo 📝 Adding all files to Git...
git add .

REM Commit changes
set /p commit_msg="Enter commit message (default: Add monitoring features and update mata pelajaran): "
if "%commit_msg%"=="" set commit_msg=Add monitoring features and update mata pelajaran
echo 💾 Committing changes...
git commit -m "%commit_msg%"

REM Push to GitHub
echo ⬆️ Pushing to GitHub...
git push origin main

echo.
echo ✅ New features pushed to GitHub!
echo.
echo 🚀 Railway will auto-deploy or:
echo 1. Go to Railway Dashboard
echo 2. Wait for auto-deployment
echo 3. Test new features:
echo.
echo 👨‍💼 Admin Features:
echo - Dashboard → "Lihat Jurnal Hari Ini"
echo - Dashboard → "Lihat Tugas Aktif"
echo.
echo 👨‍🏫 Guru Features:
echo - Dashboard → "Buat Jurnal"
echo - Dashboard → "Buat Tugas"
echo.
echo 📚 New Mata Pelajaran:
echo - Akidah Akhlak, Alquran Hadits, Fiqih
echo - Bahasa Arab, Sejarah Kebudayaan Islam
echo - Matematika Lanjut, PJOK, Prakarya
echo - Seni Budaya, Bimbingan Konseling
echo.
echo 📖 Read FITUR_BARU.md for complete guide
echo ==========================================

pause
