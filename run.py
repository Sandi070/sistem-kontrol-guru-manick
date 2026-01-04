#!/usr/bin/env python3
"""
Sistem Kontrol Guru - MAN Insan Cendekia Kota Kendari
Aplikasi untuk monitoring kehadiran, jurnal pembelajaran, dan tugas guru
"""

from app import app, db, Guru, generate_password_hash

def create_sample_data():
    """Membuat data contoh untuk testing"""
    with app.app_context():
        # Buat tabel jika belum ada
        db.create_all()
        
        # Cek apakah sudah ada data
        if Guru.query.count() > 0:
            print("Database sudah berisi data.")
            return
        
        # Buat admin default
        admin = Guru(
            nip='admin123',
            nama='Administrator Sistem',
            mata_pelajaran='Sistem',
            email='admin@manic.sch.id',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        
        # Buat beberapa guru contoh
        guru_contoh = [
            {
                'nip': '196801011990031001',
                'nama': 'Dr. Ahmad Hidayat, S.Pd., M.Pd.',
                'mata_pelajaran': 'Matematika',
                'email': 'ahmad.hidayat@manic.sch.id',
                'password': 'guru123'
            },
            {
                'nip': '197205151998022001',
                'nama': 'Siti Nurhaliza, S.Si., M.Pd.',
                'mata_pelajaran': 'Fisika',
                'email': 'siti.nurhaliza@manic.sch.id',
                'password': 'guru123'
            },
            {
                'nip': '198003102005011002',
                'nama': 'Muhammad Rizki, S.Pd., M.Pd.',
                'mata_pelajaran': 'Kimia',
                'email': 'muhammad.rizki@manic.sch.id',
                'password': 'guru123'
            },
            {
                'nip': '198507202010012003',
                'nama': 'Fatimah Azzahra, S.Pd.',
                'mata_pelajaran': 'Biologi',
                'email': 'fatimah.azzahra@manic.sch.id',
                'password': 'guru123'
            },
            {
                'nip': '199001152015031004',
                'nama': 'Andi Pratama, S.Pd.',
                'mata_pelajaran': 'Bahasa Indonesia',
                'email': 'andi.pratama@manic.sch.id',
                'password': 'guru123'
            }
        ]
        
        for data_guru in guru_contoh:
            guru = Guru(
                nip=data_guru['nip'],
                nama=data_guru['nama'],
                mata_pelajaran=data_guru['mata_pelajaran'],
                email=data_guru['email'],
                password_hash=generate_password_hash(data_guru['password']),
                role='guru'
            )
            db.session.add(guru)
        
        db.session.commit()
        print("✅ Data contoh berhasil dibuat!")
        print("\n📋 Akun Login:")
        print("👨‍💼 Admin: NIP=admin123, Password=admin123")
        print("👨‍🏫 Guru: NIP=[NIP guru], Password=guru123")

if __name__ == '__main__':
    print("🏫 Sistem Kontrol Guru - MAN Insan Cendekia Kota Kendari")
    print("=" * 60)
    
    # Buat data contoh
    create_sample_data()
    
    print("\n🚀 Menjalankan aplikasi...")
    print("📱 Akses aplikasi di: http://localhost:5000")
    print("📱 Untuk akses dari HP: http://[IP-KOMPUTER]:5000")
    print("\n⚠️  Tekan Ctrl+C untuk menghentikan aplikasi")
    print("=" * 60)
    
    # Jalankan aplikasi
    app.run(debug=True, host='0.0.0.0', port=5000)