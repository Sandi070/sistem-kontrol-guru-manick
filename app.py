import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import qrcode
import io
import base64
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Konfigurasi untuk production dan development
if os.environ.get('DATABASE_URL'):
    # Production (Railway/Heroku/Render)
    database_url = os.environ.get('DATABASE_URL')
    # Fix untuk Railway PostgreSQL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Development (Local)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///man_ic_system.db'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'man-ic-kendari-2025-production')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# === MODEL DATABASE ===
class Guru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    mata_pelajaran = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='guru')  # guru, admin
    qr_code = db.Column(db.Text)  # Base64 QR code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relasi
    kehadiran = db.relationship('Kehadiran', backref='guru', lazy=True)
    jurnal = db.relationship('JurnalPembelajaran', backref='guru', lazy=True)
    tugas = db.relationship('Tugas', backref='guru', lazy=True)

class JadwalMengajar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guru_id = db.Column(db.Integer, db.ForeignKey('guru.id'), nullable=False)
    hari = db.Column(db.String(10), nullable=False)  # Senin, Selasa, dst
    jam_mulai = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    mata_pelajaran = db.Column(db.String(50), nullable=False)
    
class Kehadiran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guru_id = db.Column(db.Integer, db.ForeignKey('guru.id'), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    jam_masuk = db.Column(db.DateTime)
    jam_keluar = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='hadir')  # hadir, tidak_hadir, terlambat
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JurnalPembelajaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guru_id = db.Column(db.Integer, db.ForeignKey('guru.id'), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    mata_pelajaran = db.Column(db.String(50), nullable=False)
    materi = db.Column(db.Text, nullable=False)
    metode_pembelajaran = db.Column(db.String(100))
    siswa_hadir = db.Column(db.Integer, default=0)
    siswa_tidak_hadir = db.Column(db.Integer, default=0)
    catatan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Tugas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guru_id = db.Column(db.Integer, db.ForeignKey('guru.id'), nullable=False)
    judul = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    mata_pelajaran = db.Column(db.String(50), nullable=False)
    tanggal_diberikan = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='aktif')  # aktif, selesai
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# === FUNGSI HELPER ===
def generate_qr_code(data):
    """Generate QR code dan return base64 string"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

def get_hari_ini():
    """Return nama hari dalam bahasa Indonesia"""
    hari_dict = {
        0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 
        4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'
    }
    return hari_dict[datetime.now().weekday()]

def check_jadwal_mengajar(guru_id):
    """Cek apakah guru sedang dalam jam mengajar"""
    hari_ini = get_hari_ini()
    waktu_sekarang = datetime.now().time()
    
    jadwal = JadwalMengajar.query.filter_by(
        guru_id=guru_id, 
        hari=hari_ini
    ).filter(
        JadwalMengajar.jam_mulai <= waktu_sekarang,
        JadwalMengajar.jam_selesai >= waktu_sekarang
    ).first()
    
    return jadwal

# === ROUTES ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nip = request.form['nip']
        password = request.form['password']
        
        guru = Guru.query.filter_by(nip=nip).first()
        
        if guru and check_password_hash(guru.password_hash, password):
            session['user_id'] = guru.id
            session['user_role'] = guru.role
            session['user_name'] = guru.nama
            
            if guru.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('guru_dashboard'))
        else:
            flash('NIP atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/guru/dashboard')
def guru_dashboard():
    if 'user_id' not in session or session.get('user_role') != 'guru':
        return redirect(url_for('login'))
    
    guru = Guru.query.get(session['user_id'])
    
    # Cek kehadiran hari ini
    kehadiran_hari_ini = Kehadiran.query.filter_by(
        guru_id=guru.id,
        tanggal=datetime.now().date()
    ).first()
    
    # Cek jadwal mengajar
    jadwal_sekarang = check_jadwal_mengajar(guru.id)
    
    # Tugas yang belum selesai
    tugas_aktif = Tugas.query.filter_by(
        guru_id=guru.id,
        status='aktif'
    ).count()
    
    return render_template('guru_dashboard.html', 
                         guru=guru,
                         kehadiran_hari_ini=kehadiran_hari_ini,
                         jadwal_sekarang=jadwal_sekarang,
                         tugas_aktif=tugas_aktif,
                         today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    # Statistik untuk dashboard admin
    total_guru = Guru.query.filter_by(role='guru').count()
    
    # Kehadiran hari ini
    kehadiran_hari_ini = db.session.query(Kehadiran).filter_by(
        tanggal=datetime.now().date()
    ).count()
    
    # Guru yang sedang mengajar
    hari_ini = get_hari_ini()
    waktu_sekarang = datetime.now().time()
    
    guru_mengajar = db.session.query(JadwalMengajar).filter_by(
        hari=hari_ini
    ).filter(
        JadwalMengajar.jam_mulai <= waktu_sekarang,
        JadwalMengajar.jam_selesai >= waktu_sekarang
    ).count()
    
    return render_template('admin_dashboard.html',
                         total_guru=total_guru,
                         kehadiran_hari_ini=kehadiran_hari_ini,
                         guru_mengajar=guru_mengajar)

# API untuk scan barcode
@app.route('/api/scan', methods=['POST'])
def scan_barcode():
    data = request.get_json()
    qr_data = data.get('qr_data')
    
    if not qr_data:
        return jsonify({'success': False, 'message': 'Data QR tidak valid'})
    
    # Parse QR data (format: "GURU_ID:NIP")
    try:
        guru_id = int(qr_data.split(':')[0])
        guru = Guru.query.get(guru_id)
        
        if not guru:
            return jsonify({'success': False, 'message': 'Guru tidak ditemukan'})
        
        # Cek kehadiran hari ini
        kehadiran = Kehadiran.query.filter_by(
            guru_id=guru.id,
            tanggal=datetime.now().date()
        ).first()
        
        if not kehadiran:
            # Absen masuk
            kehadiran = Kehadiran(
                guru_id=guru.id,
                tanggal=datetime.now().date(),
                jam_masuk=datetime.now(),
                status='hadir'
            )
            db.session.add(kehadiran)
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': f'Selamat datang {guru.nama}! Absen masuk berhasil.',
                'type': 'masuk'
            })
        else:
            # Absen keluar
            if not kehadiran.jam_keluar:
                kehadiran.jam_keluar = datetime.now()
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Sampai jumpa {guru.nama}! Absen keluar berhasil.',
                    'type': 'keluar'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Anda sudah absen keluar hari ini.'
                })
                
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error: ' + str(e)})

# API untuk generate QR code
@app.route('/api/generate-qr', methods=['POST'])
def generate_qr():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    guru = Guru.query.get(session['user_id'])
    if not guru:
        return jsonify({'success': False, 'message': 'Guru tidak ditemukan'})
    
    # Generate QR code dengan format: "GURU_ID:NIP"
    qr_data = f"{guru.id}:{guru.nip}"
    qr_code_base64 = generate_qr_code(qr_data)
    
    guru.qr_code = qr_code_base64
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'QR Code berhasil dibuat'})

# API untuk tambah guru (admin only)
@app.route('/api/tambah-guru', methods=['POST'])
def tambah_guru():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    
    # Validasi data
    required_fields = ['nip', 'nama', 'mata_pelajaran', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} harus diisi'})
    
    # Cek apakah NIP atau email sudah ada
    existing_guru = Guru.query.filter(
        (Guru.nip == data['nip']) | (Guru.email == data['email'])
    ).first()
    
    if existing_guru:
        return jsonify({'success': False, 'message': 'NIP atau email sudah terdaftar'})
    
    # Buat guru baru
    guru_baru = Guru(
        nip=data['nip'],
        nama=data['nama'],
        mata_pelajaran=data['mata_pelajaran'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='guru'
    )
    
    db.session.add(guru_baru)
    db.session.flush()  # Flush untuk mendapatkan ID
    
    # Generate QR code setelah ID tersedia
    qr_data = f"{guru_baru.id}:{guru_baru.nip}"
    guru_baru.qr_code = generate_qr_code(qr_data)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Guru berhasil ditambahkan'})

# API untuk daftar guru (admin only)
@app.route('/api/daftar-guru')
def daftar_guru():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Query semua guru kecuali admin
    guru_list = Guru.query.filter_by(role='guru').all()
    
    data = []
    for guru in guru_list:
        data.append({
            'id': guru.id,
            'nama': guru.nama,
            'nip': guru.nip,
            'mata_pelajaran': guru.mata_pelajaran,
            'email': guru.email,
            'qr_code': guru.qr_code,
            'created_at': guru.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify({'success': True, 'data': data})

# API untuk kehadiran hari ini (admin only)
@app.route('/api/kehadiran-hari-ini')
def kehadiran_hari_ini():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Query kehadiran hari ini dengan join ke tabel guru
    kehadiran_list = db.session.query(Kehadiran, Guru).join(Guru).filter(
        Kehadiran.tanggal == datetime.now().date()
    ).all()
    
    data = []
    for kehadiran, guru in kehadiran_list:
        data.append({
            'nama': guru.nama,
            'nip': guru.nip,
            'mata_pelajaran': guru.mata_pelajaran,
            'jam_masuk': kehadiran.jam_masuk.strftime('%H:%M') if kehadiran.jam_masuk else '-',
            'jam_keluar': kehadiran.jam_keluar.strftime('%H:%M') if kehadiran.jam_keluar else '-',
            'status': kehadiran.status
        })
    
    return jsonify({'success': True, 'data': data})

# API untuk notifikasi (akan dipanggil secara berkala)
@app.route('/api/check-notifications')
def check_notifications():
    notifications = []
    
    # Cek guru yang seharusnya sudah masuk tapi belum absen
    hari_ini = get_hari_ini()
    waktu_sekarang = datetime.now().time()
    
    # Ambil jadwal yang sudah dimulai tapi guru belum absen
    jadwal_aktif = db.session.query(JadwalMengajar, Guru).join(Guru).filter(
        JadwalMengajar.hari == hari_ini,
        JadwalMengajar.jam_mulai <= waktu_sekarang
    ).all()
    
    for jadwal, guru in jadwal_aktif:
        # Cek apakah guru sudah absen hari ini
        kehadiran = Kehadiran.query.filter_by(
            guru_id=guru.id,
            tanggal=datetime.now().date()
        ).first()
        
        if not kehadiran:
            notifications.append({
                'type': 'warning',
                'message': f'{guru.nama} belum absen masuk. Jadwal mengajar {jadwal.mata_pelajaran} kelas {jadwal.kelas} dimulai {jadwal.jam_mulai.strftime("%H:%M")}'
            })
    
    return jsonify({'notifications': notifications})

# API untuk monitoring jurnal pembelajaran (admin only)
@app.route('/api/monitoring-jurnal')
def monitoring_jurnal():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Query jurnal hari ini dengan join ke tabel guru
    jurnal_list = db.session.query(JurnalPembelajaran, Guru).join(Guru).filter(
        JurnalPembelajaran.tanggal == datetime.now().date()
    ).order_by(JurnalPembelajaran.created_at.desc()).all()
    
    data = []
    for jurnal, guru in jurnal_list:
        data.append({
            'id': jurnal.id,
            'guru_nama': guru.nama,
            'guru_nip': guru.nip,
            'kelas': jurnal.kelas,
            'mata_pelajaran': jurnal.mata_pelajaran,
            'materi': jurnal.materi,
            'metode_pembelajaran': jurnal.metode_pembelajaran,
            'siswa_hadir': jurnal.siswa_hadir,
            'siswa_tidak_hadir': jurnal.siswa_tidak_hadir,
            'catatan': jurnal.catatan,
            'waktu_input': jurnal.created_at.strftime('%H:%M')
        })
    
    return jsonify({'success': True, 'data': data})

# API untuk monitoring tugas (admin only)
@app.route('/api/monitoring-tugas')
def monitoring_tugas():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Query tugas aktif dengan join ke tabel guru
    tugas_list = db.session.query(Tugas, Guru).join(Guru).filter(
        Tugas.status == 'aktif'
    ).order_by(Tugas.created_at.desc()).all()
    
    data = []
    for tugas, guru in tugas_list:
        # Hitung sisa hari deadline
        sisa_hari = (tugas.deadline - datetime.now().date()).days
        status_deadline = 'normal'
        if sisa_hari < 0:
            status_deadline = 'overdue'
        elif sisa_hari <= 2:
            status_deadline = 'urgent'
        
        data.append({
            'id': tugas.id,
            'guru_nama': guru.nama,
            'guru_nip': guru.nip,
            'judul': tugas.judul,
            'deskripsi': tugas.deskripsi,
            'kelas': tugas.kelas,
            'mata_pelajaran': tugas.mata_pelajaran,
            'tanggal_diberikan': tugas.tanggal_diberikan.strftime('%Y-%m-%d'),
            'deadline': tugas.deadline.strftime('%Y-%m-%d'),
            'sisa_hari': sisa_hari,
            'status_deadline': status_deadline,
            'waktu_dibuat': tugas.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify({'success': True, 'data': data})

# API untuk submit jurnal pembelajaran (guru)
@app.route('/api/submit-jurnal', methods=['POST'])
def submit_jurnal():
    if 'user_id' not in session or session.get('user_role') != 'guru':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    
    # Validasi data
    required_fields = ['tanggal', 'kelas', 'mata_pelajaran', 'materi']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} harus diisi'})
    
    try:
        # Buat jurnal baru
        jurnal = JurnalPembelajaran(
            guru_id=session['user_id'],
            tanggal=datetime.strptime(data['tanggal'], '%Y-%m-%d').date(),
            kelas=data['kelas'],
            mata_pelajaran=data['mata_pelajaran'],
            materi=data['materi'],
            metode_pembelajaran=data.get('metode_pembelajaran', ''),
            siswa_hadir=int(data.get('siswa_hadir', 0)),
            siswa_tidak_hadir=int(data.get('siswa_tidak_hadir', 0)),
            catatan=data.get('catatan', '')
        )
        
        db.session.add(jurnal)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Jurnal berhasil disimpan'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# API untuk submit tugas (guru)
@app.route('/api/submit-tugas', methods=['POST'])
def submit_tugas():
    if 'user_id' not in session or session.get('user_role') != 'guru':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    
    # Validasi data
    required_fields = ['judul', 'deskripsi', 'kelas', 'mata_pelajaran', 'tanggal_diberikan', 'deadline']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} harus diisi'})
    
    try:
        # Buat tugas baru
        tugas = Tugas(
            guru_id=session['user_id'],
            judul=data['judul'],
            deskripsi=data['deskripsi'],
            kelas=data['kelas'],
            mata_pelajaran=data['mata_pelajaran'],
            tanggal_diberikan=datetime.strptime(data['tanggal_diberikan'], '%Y-%m-%d').date(),
            deadline=datetime.strptime(data['deadline'], '%Y-%m-%d').date(),
            status='aktif'
        )
        
        db.session.add(tugas)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tugas berhasil disimpan'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# Route untuk menambah jadwal mengajar (admin)
@app.route('/admin/jadwal', methods=['GET', 'POST'])
def kelola_jadwal():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Logic untuk menambah jadwal
        pass
    
    # Tampilkan form jadwal
    guru_list = Guru.query.filter_by(role='guru').all()
    return render_template('admin_jadwal.html', guru_list=guru_list)

# Inisialisasi database dan data default
def init_database():
    """Inisialisasi database dan buat data default"""
    db.create_all()
    
    # Buat admin default jika belum ada
    admin = Guru.query.filter_by(role='admin').first()
    if not admin:
        admin = Guru(
            nip='admin123',
            nama='Administrator Sistem',
            mata_pelajaran='Sistem',
            email='admin@manic.sch.id',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin default dibuat: NIP=admin123, Password=admin123")
    
    # Buat sample guru jika belum ada
    if Guru.query.filter_by(role='guru').count() == 0:
        sample_guru = [
            {
                'nip': '196801011990031001',
                'nama': 'Dr. Ahmad Hidayat, S.Pd., M.Pd.',
                'mata_pelajaran': 'Matematika',
                'email': 'ahmad.hidayat@manic.sch.id'
            },
            {
                'nip': '197205151998022001',
                'nama': 'Siti Nurhaliza, S.Si., M.Pd.',
                'mata_pelajaran': 'Fisika',
                'email': 'siti.nurhaliza@manic.sch.id'
            },
            {
                'nip': '198003102005011002',
                'nama': 'Muhammad Rizki, S.Pd., M.Pd.',
                'mata_pelajaran': 'Kimia',
                'email': 'muhammad.rizki@manic.sch.id'
            }
        ]
        
        for data in sample_guru:
            guru = Guru(
                nip=data['nip'],
                nama=data['nama'],
                mata_pelajaran=data['mata_pelajaran'],
                email=data['email'],
                password_hash=generate_password_hash('guru123'),
                role='guru'
            )
            db.session.add(guru)
            db.session.flush()  # Get ID
            
            # Generate QR code
            qr_data = f"{guru.id}:{guru.nip}"
            guru.qr_code = generate_qr_code(qr_data)
        
        db.session.commit()
        print("✅ Sample guru berhasil dibuat dengan password: guru123")

# Inisialisasi untuk production
with app.app_context():
    init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
