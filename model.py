from app import db
from sqlalchemy import ForeignKey

class M_Pinjam(db.Model):
    __tablename__ = 'tb_pinjam'
    KodePinjam = db.Column(db.Integer, primary_key=True)
    KodeBuku = db.Column(db.Integer, ForeignKey('tb_buku.KodeBuku'))
    NIM = db.Column(db.Integer, ForeignKey('tb_anggota.NIM'))
    TglPinjam = db.Column(db.Date)

    def __init__(self, KodePinjam, KodeBuku, NIM, TglPinjam):
        self.KodePinjam = KodePinjam
        self.KodeBuku = KodeBuku
        self.NIM = NIM
        self.TglPinjam = TglPinjam

    def __repr__(self):
        return '[%s, %s, %s, %s]' % \
        (self.KodePinjam, self.KodeBuku, self.NIM, self.TglPinjam)

class M_Kembali(db.Model):
    __tablename__ = 'tb_kembali'
    KodeKembali = db.Column(db.Integer, primary_key=True)
    KodeBuku = db.Column(db.Integer, ForeignKey('tb_buku.KodeBuku'))
    NIM = db.Column(db.Integer, ForeignKey('tb_anggota.NIM'))
    TglKembali = db.Column(db.Date)

    def __init__(self, KodeKembali, KodeBuku, NIM, TglKembali):
        self.KodeKembali = KodeKembali
        self.KodeBuku = KodeBuku
        self.NIM = NIM
        self.TglKembali = TglKembali

    def __repr__(self):
        return '[%s, %s, %s, %s]' % \
        (self.KodeKembali, self.KodeBuku, self.NIM, self.TglKembali)

class Buku(db.Model):
    __tablename__ = 'tb_buku'
    KodeBuku = db.Column(db.Integer, primary_key=True)
    Judul = db.Column(db.String(50), unique=True)
    Stok = db.Column(db.Integer)

    def __init__(self, KodeBuku, Judul, Stok):
        self.KodeBuku = KodeBuku
        self.Judul = Judul
        self.Stok = Stok

    def __repr__(self):
        return '[%s, %s, %s]' % \
        (self.KodeBuku, self.Judul, self.Stok)

class Anggota(db.Model):
    __tablename__ = 'tb_anggota'
    NIM = db.Column(db.Integer, primary_key=True)
    Nama = db.Column(db.String(50))
    Jurusan = db.Column(db.String(30))
    Username = db.Column(db.String(12), unique=True)
    Password = db.Column(db.String(30))

    def __init__(self, NIM, Nama, Jurusan, Username, Password):
        self.NIM = NIM
        self.Nama = Nama
        self.Jurusan = Jurusan
        self.Username = Username
        self.Password = Password

    def __repr__(self):
        return '[%s, %s, %s, %s, %s]' % \
        (self.NIM, self.Nama, self.Jurusan, self.Username, self.Password)        