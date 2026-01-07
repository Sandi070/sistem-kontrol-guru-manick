import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import qrcode
import io
import base64
from werkzeug.security import generate_password_hash, check_password_hash
import pytz

# Konfigurasi zona waktu WITA (UTC+8)
WITA = pytz.timezone('Asia/Makassar')

def get_wita_time():
    """Return current time in WITA timezone"""
    return datetime.now(WITA)

def get_wita_date():
    """Return current date in WITA timezone"""
    return get_wita_time().date()

def get_wita_time_only():
    """Return current time only in WITA timezone"""
    return get_wita_time().time()

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
    kelas = db.Column(db.String(10), nullable=False)  # Absensi per kelas
    mata_pelajaran = db.Column(db.String(50), nullable=False)
    jam_masuk = db.Column(db.DateTime)
    jam_keluar = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='hadir')  # hadir, tidak_hadir, terlambat
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: get_wita_time())

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
    created_at = db.Column(db.DateTime, default=lambda: get_wita_time())

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
    created_at = db.Column(db.DateTime, default=lambda: get_wita_time())

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
    return hari_dict[get_wita_time().weekday()]

def check_jadwal_mengajar(guru_id):
    """Cek apakah guru sedang dalam jam mengajar"""
    hari_ini = get_hari_ini()
    waktu_sekarang = get_wita_time_only()
    
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
        tanggal=get_wita_date()
    ).all()  # Ambil semua kehadiran hari ini (per kelas)
    
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
                         today=get_wita_date().strftime('%Y-%m-%d'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    # Statistik untuk dashboard admin
    total_guru = Guru.query.filter_by(role='guru').count()
    
    # Kehadiran hari ini
    kehadiran_hari_ini = db.session.query(Kehadiran).filter_by(
        tanggal=get_wita_date()
    ).count()
    
    # Guru yang sedang mengajar
    hari_ini = get_hari_ini()
    waktu_sekarang = get_wita_time_only()
    
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

# API untuk scan barcode - Updated untuk absensi per kelas
@app.route('/api/scan', methods=['POST'])
def scan_barcode():
    data = request.get_json()
    qr_data = data.get('qr_data')
    kelas = data.get('kelas')  # Kelas untuk absensi
    mata_pelajaran = data.get('mata_pelajaran')  # Mata pelajaran
    
    if not qr_data:
        return jsonify({'success': False, 'message': 'Data QR tidak valid'})
    
    if not kelas or not mata_pelajaran:
        return jsonify({'success': False, 'message': 'Kelas dan mata pelajaran harus diisi'})
    
    # Parse QR data (format: "GURU_ID:NIP")
    try:
        guru_id = int(qr_data.split(':')[0])
        guru = Guru.query.get(guru_id)
        
        if not guru:
            return jsonify({'success': False, 'message': 'Guru tidak ditemukan'})
        
        # Cek kehadiran untuk kelas dan mata pelajaran ini hari ini
        kehadiran = Kehadiran.query.filter_by(
            guru_id=guru.id,
            tanggal=get_wita_date(),
            kelas=kelas,
            mata_pelajaran=mata_pelajaran
        ).first()
        
        if not kehadiran:
            # Absen masuk untuk kelas ini
            kehadiran = Kehadiran(
                guru_id=guru.id,
                tanggal=get_wita_date(),
                kelas=kelas,
                mata_pelajaran=mata_pelajaran,
                jam_masuk=get_wita_time(),
                status='hadir'
            )
            db.session.add(kehadiran)
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': f'Selamat datang {guru.nama}! Absen masuk kelas {kelas} ({mata_pelajaran}) berhasil.',
                'type': 'masuk'
            })
        else:
            # Absen keluar untuk kelas ini
            if not kehadiran.jam_keluar:
                kehadiran.jam_keluar = get_wita_time()
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Sampai jumpa {guru.nama}! Absen keluar kelas {kelas} ({mata_pelajaran}) berhasil.',
                    'type': 'keluar'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': f'Anda sudah absen keluar untuk kelas {kelas} hari ini.'
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

# API untuk kehadiran hari ini (admin only) - Updated untuk per kelas
@app.route('/api/kehadiran-hari-ini')
def kehadiran_hari_ini():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Query kehadiran hari ini dengan join ke tabel guru
    kehadiran_list = db.session.query(Kehadiran, Guru).join(Guru).filter(
        Kehadiran.tanggal == get_wita_date()
    ).order_by(Kehadiran.created_at.desc()).all()
    
    data = []
    for kehadiran, guru in kehadiran_list:
        data.append({
            'nama': guru.nama,
            'nip': guru.nip,
            'kelas': kehadiran.kelas,
            'mata_pelajaran': kehadiran.mata_pelajaran,
            'jam_masuk': kehadiran.jam_masuk.strftime('%H:%M') if kehadiran.jam_masuk else '-',
            'jam_keluar': kehadiran.jam_keluar.strftime('%H:%M') if kehadiran.jam_keluar else '-',
            'status': kehadiran.status,
            'keterangan': kehadiran.keterangan or '-'
        })
    
    return jsonify({'success': True, 'data': data})

# API untuk hapus guru (admin only)
@app.route('/api/hapus-guru/<int:guru_id>', methods=['DELETE'])
def hapus_guru(guru_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        guru = Guru.query.get(guru_id)
        if not guru:
            return jsonify({'success': False, 'message': 'Guru tidak ditemukan'})
        
        if guru.role == 'admin':
            return jsonify({'success': False, 'message': 'Tidak dapat menghapus admin'})
        
        # Hapus data terkait
        Kehadiran.query.filter_by(guru_id=guru_id).delete()
        JurnalPembelajaran.query.filter_by(guru_id=guru_id).delete()
        Tugas.query.filter_by(guru_id=guru_id).delete()
        JadwalMengajar.query.filter_by(guru_id=guru_id).delete()
        
        # Hapus guru
        db.session.delete(guru)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Guru berhasil dihapus'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# API untuk edit password guru (admin only)
@app.route('/api/edit-password', methods=['POST'])
def edit_password():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    guru_id = data.get('guru_id')
    new_password = data.get('new_password')
    
    if not guru_id or not new_password:
        return jsonify({'success': False, 'message': 'Guru ID dan password baru harus diisi'})
    
    try:
        guru = Guru.query.get(guru_id)
        if not guru:
            return jsonify({'success': False, 'message': 'Guru tidak ditemukan'})
        
        guru.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password berhasil diubah'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# API untuk print jurnal pembelajaran
@app.route('/api/print-jurnal')
def print_jurnal():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Parameter filter
    tanggal_mulai = request.args.get('tanggal_mulai')
    tanggal_selesai = request.args.get('tanggal_selesai')
    guru_id = request.args.get('guru_id')
    
    # Base query
    query = db.session.query(JurnalPembelajaran, Guru).join(Guru)
    
    # Filter berdasarkan role
    if session.get('user_role') == 'guru':
        query = query.filter(JurnalPembelajaran.guru_id == session['user_id'])
    elif guru_id:
        query = query.filter(JurnalPembelajaran.guru_id == guru_id)
    
    # Filter tanggal
    if tanggal_mulai:
        query = query.filter(JurnalPembelajaran.tanggal >= tanggal_mulai)
    if tanggal_selesai:
        query = query.filter(JurnalPembelajaran.tanggal <= tanggal_selesai)
    
    jurnal_list = query.order_by(JurnalPembelajaran.tanggal.desc()).all()
    
    data = []
    for jurnal, guru in jurnal_list:
        data.append({
            'tanggal': jurnal.tanggal.strftime('%Y-%m-%d'),
            'guru_nama': guru.nama,
            'guru_nip': guru.nip,
            'kelas': jurnal.kelas,
            'mata_pelajaran': jurnal.mata_pelajaran,
            'materi': jurnal.materi,
            'metode_pembelajaran': jurnal.metode_pembelajaran,
            'siswa_hadir': jurnal.siswa_hadir,
            'siswa_tidak_hadir': jurnal.siswa_tidak_hadir,
            'catatan': jurnal.catatan,
            'waktu_input': jurnal.created_at.strftime('%Y-%m-%d %H:%M')
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
        JurnalPembelajaran.tanggal == get_wita_date()
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
        sisa_hari = (tugas.deadline - get_wita_date()).days
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

# API untuk daftar jadwal mengajar (admin only)
@app.route('/api/jadwal-mengajar')
def jadwal_mengajar():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Query jadwal dengan join ke tabel guru
    jadwal_list = db.session.query(JadwalMengajar, Guru).join(Guru).order_by(
        JadwalMengajar.hari, JadwalMengajar.jam_mulai
    ).all()
    
    data = []
    for jadwal, guru in jadwal_list:
        data.append({
            'id': jadwal.id,
            'guru_id': guru.id,
            'guru_nama': guru.nama,
            'guru_nip': guru.nip,
            'hari': jadwal.hari,
            'jam_mulai': jadwal.jam_mulai.strftime('%H:%M'),
            'jam_selesai': jadwal.jam_selesai.strftime('%H:%M'),
            'kelas': jadwal.kelas,
            'mata_pelajaran': jadwal.mata_pelajaran
        })
    
    return jsonify({'success': True, 'data': data})

# API untuk tambah jadwal mengajar (admin only)
@app.route('/api/tambah-jadwal', methods=['POST'])
def tambah_jadwal():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    
    # Validasi data
    required_fields = ['guru_id', 'hari', 'jam_mulai', 'jam_selesai', 'kelas', 'mata_pelajaran']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} harus diisi'})
    
    try:
        # Cek konflik jadwal
        existing_jadwal = JadwalMengajar.query.filter_by(
            hari=data['hari'],
            kelas=data['kelas']
        ).filter(
            JadwalMengajar.jam_mulai < datetime.strptime(data['jam_selesai'], '%H:%M').time(),
            JadwalMengajar.jam_selesai > datetime.strptime(data['jam_mulai'], '%H:%M').time()
        ).first()
        
        if existing_jadwal:
            return jsonify({'success': False, 'message': f'Konflik jadwal! Kelas {data["kelas"]} sudah ada jadwal pada {data["hari"]} jam tersebut'})
        
        # Buat jadwal baru
        jadwal = JadwalMengajar(
            guru_id=int(data['guru_id']),
            hari=data['hari'],
            jam_mulai=datetime.strptime(data['jam_mulai'], '%H:%M').time(),
            jam_selesai=datetime.strptime(data['jam_selesai'], '%H:%M').time(),
            kelas=data['kelas'],
            mata_pelajaran=data['mata_pelajaran']
        )
        
        db.session.add(jadwal)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Jadwal berhasil ditambahkan'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# API untuk hapus jadwal mengajar (admin only)
@app.route('/api/hapus-jadwal/<int:jadwal_id>', methods=['DELETE'])
def hapus_jadwal(jadwal_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        jadwal = JadwalMengajar.query.get(jadwal_id)
        if not jadwal:
            return jsonify({'success': False, 'message': 'Jadwal tidak ditemukan'})
        
        db.session.delete(jadwal)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Jadwal berhasil dihapus'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# API untuk jadwal guru (guru only)
@app.route('/api/jadwal-guru')
def jadwal_guru():
    if 'user_id' not in session or session.get('user_role') != 'guru':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Query jadwal guru yang login
    jadwal_list = JadwalMengajar.query.filter_by(
        guru_id=session['user_id']
    ).order_by(JadwalMengajar.hari, JadwalMengajar.jam_mulai).all()
    
    data = []
    for jadwal in jadwal_list:
        data.append({
            'id': jadwal.id,
            'hari': jadwal.hari,
            'jam_mulai': jadwal.jam_mulai.strftime('%H:%M'),
            'jam_selesai': jadwal.jam_selesai.strftime('%H:%M'),
            'kelas': jadwal.kelas,
            'mata_pelajaran': jadwal.mata_pelajaran
        })
    
    return jsonify({'success': True, 'data': data})

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
            },
            {
                'nip': '198507202010012003',
                'nama': 'Ustadz Abdullah, S.Ag., M.Pd.I.',
                'mata_pelajaran': 'Akidah Akhlak',
                'email': 'abdullah@manic.sch.id'
            },
            {
                'nip': '199001152015031004',
                'nama': 'Ustadzah Fatimah, S.Pd.I., M.Pd.',
                'mata_pelajaran': 'Alquran Hadits',
                'email': 'fatimah@manic.sch.id'
            },
            {
                'nip': '199203102018011005',
                'nama': 'Ahmad Fauzi, S.Pd.I., M.H.',
                'mata_pelajaran': 'Fiqih',
                'email': 'fauzi@manic.sch.id'
            },
            {
                'nip': '198805252019032006',
                'nama': 'Dr. Khadijah, S.S., M.Pd.',
                'mata_pelajaran': 'Bahasa Arab',
                'email': 'khadijah@manic.sch.id'
            },
            {
                'nip': '199512102020121007',
                'nama': 'Umar Faruq, S.Pd.I., M.A.',
                'mata_pelajaran': 'Sejarah Kebudayaan Islam',
                'email': 'umar@manic.sch.id'
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
    
    # Buat sample jadwal mengajar jika belum ada
    if JadwalMengajar.query.count() == 0:
        # Ambil guru yang sudah dibuat
        guru_matematika = Guru.query.filter_by(mata_pelajaran='Matematika').first()
        guru_fisika = Guru.query.filter_by(mata_pelajaran='Fisika').first()
        guru_kimia = Guru.query.filter_by(mata_pelajaran='Kimia').first()
        guru_akidah = Guru.query.filter_by(mata_pelajaran='Akidah Akhlak').first()
        guru_quran = Guru.query.filter_by(mata_pelajaran='Alquran Hadits').first()
        
        sample_jadwal = []
        
        if guru_matematika:
            sample_jadwal.extend([
                {'guru_id': guru_matematika.id, 'hari': 'Senin', 'jam_mulai': '07:30', 'jam_selesai': '09:00', 'kelas': 'X-1', 'mata_pelajaran': 'Matematika'},
                {'guru_id': guru_matematika.id, 'hari': 'Rabu', 'jam_mulai': '10:15', 'jam_selesai': '11:45', 'kelas': 'XI IPA-1', 'mata_pelajaran': 'Matematika'},
                {'guru_id': guru_matematika.id, 'hari': 'Jumat', 'jam_mulai': '07:30', 'jam_selesai': '09:00', 'kelas': 'XII IPA-1', 'mata_pelajaran': 'Matematika'}
            ])
        
        if guru_fisika:
            sample_jadwal.extend([
                {'guru_id': guru_fisika.id, 'hari': 'Selasa', 'jam_mulai': '09:15', 'jam_selesai': '10:45', 'kelas': 'XI IPA-1', 'mata_pelajaran': 'Fisika'},
                {'guru_id': guru_fisika.id, 'hari': 'Kamis', 'jam_mulai': '13:00', 'jam_selesai': '14:30', 'kelas': 'XII IPA-2', 'mata_pelajaran': 'Fisika'}
            ])
        
        if guru_kimia:
            sample_jadwal.extend([
                {'guru_id': guru_kimia.id, 'hari': 'Senin', 'jam_mulai': '13:00', 'jam_selesai': '14:30', 'kelas': 'XI IPA-2', 'mata_pelajaran': 'Kimia'},
                {'guru_id': guru_kimia.id, 'hari': 'Rabu', 'jam_mulai': '07:30', 'jam_selesai': '09:00', 'kelas': 'XII IPA-1', 'mata_pelajaran': 'Kimia'}
            ])
        
        if guru_akidah:
            sample_jadwal.extend([
                {'guru_id': guru_akidah.id, 'hari': 'Selasa', 'jam_mulai': '07:30', 'jam_selesai': '09:00', 'kelas': 'X-1', 'mata_pelajaran': 'Akidah Akhlak'},
                {'guru_id': guru_akidah.id, 'hari': 'Kamis', 'jam_mulai': '09:15', 'jam_selesai': '10:45', 'kelas': 'X-2', 'mata_pelajaran': 'Akidah Akhlak'}
            ])
        
        if guru_quran:
            sample_jadwal.extend([
                {'guru_id': guru_quran.id, 'hari': 'Senin', 'jam_mulai': '09:15', 'jam_selesai': '10:45', 'kelas': 'X-1', 'mata_pelajaran': 'Alquran Hadits'},
                {'guru_id': guru_quran.id, 'hari': 'Jumat', 'jam_mulai': '09:15', 'jam_selesai': '10:45', 'kelas': 'XI IPA-1', 'mata_pelajaran': 'Alquran Hadits'}
            ])
        
        for data in sample_jadwal:
            jadwal = JadwalMengajar(
                guru_id=data['guru_id'],
                hari=data['hari'],
                jam_mulai=datetime.strptime(data['jam_mulai'], '%H:%M').time(),
                jam_selesai=datetime.strptime(data['jam_selesai'], '%H:%M').time(),
                kelas=data['kelas'],
                mata_pelajaran=data['mata_pelajaran']
            )
            db.session.add(jadwal)
        
        db.session.commit()
        print("✅ Sample jadwal mengajar berhasil dibuat")

# Inisialisasi untuk production
with app.app_context():
    init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
