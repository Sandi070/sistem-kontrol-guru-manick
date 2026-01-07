@echo off
echo 🔄 Deploying Major Updates - MAN IC Kendari
echo ===================================================

echo 📝 Fitur yang ditambahkan/diperbarui:
echo ✅ Zona Waktu WITA (UTC+8) untuk Sulawesi Tenggara
echo ✅ Kelas diperluas: X-1 s/d X-5, XI-1 s/d XI-5, XII-1 s/d XII-5
echo ✅ Absensi per kelas (bukan per hari)
echo ✅ Menu Hapus Guru (Admin)
echo ✅ Menu Edit Password Guru (Admin)
echo ✅ Print Jurnal Pembelajaran
echo ✅ Monitoring Kehadiran Aktif
echo ✅ Dashboard Guru - Kehadiran per kelas

REM Add all files
echo 📝 Adding all files to Git...
git add .

REM Commit changes
set /p commit_msg="Enter commit message (default: Update WITA timezone, per-class attendance, admin features): "
if "%commit_msg%"=="" set commit_msg=Update WITA timezone, per-class attendance, admin features
echo 💾 Committing changes...
git commit -m "%commit_msg%"

REM Push to GitHub
echo ⬆️ Pushing to GitHub...
git push origin main

echo.
echo ✅ Updates pushed to GitHub!
echo.
echo 🚀 Railway will auto-deploy or:
echo 1. Go to Railway Dashboard
echo 2. Wait for auto-deployment
echo 3. Test new features:
echo.
echo 👨‍💼 Admin Features:
echo - Monitoring Kehadiran (per kelas)
echo - Hapus Guru dari Daftar Guru
echo - Edit Password Guru
echo - Print Jurnal Pembelajaran (dengan filter periode)
echo.
echo 👨‍🏫 Guru Features:
echo - Absensi per kelas yang diajar
echo - Lihat kehadiran hari ini per kelas
echo - Semua waktu dalam zona WITA
echo.
echo 🕐 Zona Waktu:
echo - Semua timestamp menggunakan WITA (UTC+8)
echo - Sesuai dengan Sulawesi Tenggara
echo.
echo � KelasF Tersedia:
echo - X-1, X-2, X-3, X-4, X-5
echo - XI-1, XI-2, XI-3, XI-4, XI-5
echo - XII-1, XII-2, XII-3, XII-4, XII-5
echo.
echo 📖 Read UPDATE_FITUR_WITA.md for complete guide
echo ===================================================

pause
