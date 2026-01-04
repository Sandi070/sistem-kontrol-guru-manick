@echo off
echo 🆕 Deploying Jadwal Mengajar Feature - MAN IC Kendari
echo ===================================================

echo 📝 Fitur jadwal mengajar yang ditambahkan:
echo ✅ Manajemen Jadwal Mengajar (Admin)
echo ✅ Tambah/Hapus Jadwal dengan validasi konflik
echo ✅ Lihat Jadwal Guru (Guru)
echo ✅ Jadwal Hari Ini (Guru)
echo ✅ Sample data jadwal mengajar
echo ✅ Auto-fill mata pelajaran berdasarkan guru
echo ✅ Integrasi dengan sistem absensi

REM Add all files
echo 📝 Adding all files to Git...
git add .

REM Commit changes
set /p commit_msg="Enter commit message (default: Add jadwal mengajar feature): "
if "%commit_msg%"=="" set commit_msg=Add jadwal mengajar feature
echo 💾 Committing changes...
git commit -m "%commit_msg%"

REM Push to GitHub
echo ⬆️ Pushing to GitHub...
git push origin main

echo.
echo ✅ Jadwal mengajar feature pushed to GitHub!
echo.
echo 🚀 Railway will auto-deploy or:
echo 1. Go to Railway Dashboard
echo 2. Wait for auto-deployment
echo 3. Test new jadwal features:
echo.
echo 👨‍💼 Admin Features:
echo - Dashboard → "Lihat Jadwal"
echo - Dashboard → "Tambah Jadwal" (with conflict validation)
echo - Hapus jadwal dari tabel
echo.
echo 👨‍🏫 Guru Features:
echo - Dashboard → "Lihat Jadwal" (all schedule)
echo - Dashboard → "Jadwal Hari Ini" (today only)
echo.
echo 📊 Sample Jadwal:
echo - Matematika: Senin 07:30-09:00 (X-1)
echo - Fisika: Selasa 09:15-10:45 (XI IPA-1)
echo - Akidah Akhlak: Selasa 07:30-09:00 (X-1)
echo - Alquran Hadits: Senin 09:15-10:45 (X-1)
echo - Dan lainnya...
echo.
echo 📖 Read FITUR_BARU.md for complete guide
echo ===================================================

pause
