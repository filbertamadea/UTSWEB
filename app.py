from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime

app = Flask(__name__, template_folder="templates")
app.config.from_pyfile('config.cfg')
app.config['SECRET_KEY'] = '@#$123456&*()'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_book'
mysql = MySQL(app)
db = SQLAlchemy(app)
from model import Buku, Anggota, M_Kembali, M_Pinjam

@app.route('/')
def root():
    return render_template(\
    'landingpage.html',\
    dosen=app.config['DOSEN_TERCINTA'],\
    namakel=app.config['NAMA_KELOMPOK'],\
    namaweb=app.config['NAMA_WEB'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = '' #Variabel pesan
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] #akses form username
        password = request.form['password'] #akses form password
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tb_anggota WHERE Username = %s AND Password = %s', (username, password,))
        tb_anggota = cursor.fetchone() #fetch data
        if tb_anggota:
            session['loggedin'] = True
            session['NIM'] = tb_anggota['NIM']
            session['Username'] = tb_anggota['Username']
            msg = 'Logged in successfully !'
            return render_template('news.html',\
                                    dosen=app.config['DOSEN_TERCINTA'],\
                                    namakel=app.config['NAMA_KELOMPOK'],\
                                    namaweb=app.config['NAMA_WEB'], msg = msg)
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',\
    dosen=app.config['DOSEN_TERCINTA'],\
    namakel=app.config['NAMA_KELOMPOK'],\
    namaweb=app.config['NAMA_WEB'], msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form and 'NIM' in request.form :
        Username = request.form['Username']
        Password = request.form['Password']
        NIM = request.form['NIM']
        Nama = request.form['Nama']
        Jurusan = request.form['Jurusan']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tb_anggota WHERE Username = % s', (Username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'Username must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO tb_anggota VALUES (% s, % s, % s, % s, % s)', (NIM, Nama, Jurusan, Username, Password, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html',\
    dosen=app.config['DOSEN_TERCINTA'],\
    namakel=app.config['NAMA_KELOMPOK'],\
    namaweb=app.config['NAMA_WEB'], msg = msg)

@app.route('/login/home')
def news():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('news.html', Username=session['Username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/login/account',methods=['POST','GET'])
def account():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        data = Anggota.query.filter_by(NIM = session['NIM']).first()
        # Show the profile page with account info
        if request.method == 'POST':
            data.Username = request.form.get("Username")
            data.nama = request.form.get("Nama")
            data.jurusan = request.form.get("Jurusan")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute ("""
                            UPDATE tb_anggota
                            SET Username=%s, Nama=%s, Jurusan=%s
                            WHERE Username=%s
                            """, (data.Username, data.nama, data.jurusan, data.Username))
            mysql.connection.commit()
            msg = 'Refresh untuk melihat perubahan!'
            return render_template('account.html', tb_anggota=data, msg = msg)
        return render_template('account.html', tb_anggota=data)
    # User is not loggedin redirect to login page
    else: return redirect(url_for('login'))
  
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route("/peminjaman",methods=['GET','POST'])
def peminjaman():
    #fetch user
    username = 'jsmith'
    user = Anggota.query.filter_by(Username = username).first()
    if user:
        return render_template('peminjaman.html', name=user.Nama, nim=user.NIM, book_list=Buku.query.filter(Buku.Stok != 0).all())
    else:
        #shouldve render/redirect back to login but okay lol
        return render_template('login.html')

@app.route("/pengembalian",methods=['GET','POST'])
def pengembalian():
        #fetch user
    username = 'jsmith'
    user = Anggota.query.filter_by(Username = username).first()
    if user:
        #join table
        results = db.session.query(M_Pinjam.NIM, Buku.Judul, Buku.KodeBuku, M_Pinjam.TglPinjam).\
            join(Buku, Buku.KodeBuku == M_Pinjam.KodeBuku).\
            filter(M_Pinjam.NIM == user.NIM).all()
        for res in results:
            print(res.KodeBuku)
        return render_template('pengembalian.html', name=user.Nama, nim=user.NIM, borrow_list=results)
    else:
        #shouldve render/redirect back to login but okay lol
        return render_template('login.html')

# FUNCTIONALITY BUKU
@app.route('/pinjamBuku/<KodeBuku>',methods=['GET','POST'])
def pinjamBuku(KodeBuku):
    #fetch user || USE SESSION INSTEAD
    username = 'jsmith'
    user = Anggota.query.filter_by(Username = username).first()
    
    #create date
    x = datetime.datetime.now()

    #fetch last index INT
    last_item = M_Pinjam.query.order_by(M_Pinjam.KodePinjam.desc()).first()
    if last_item is not None:
        last_item = last_item.KodePinjam 

    #fetch targeted row from BUKU
    buku = Buku.query.filter_by(KodeBuku=KodeBuku).first()

    #check if already borrow
    check = True if (M_Pinjam.query.filter_by(NIM=user.NIM,KodeBuku=KodeBuku).first()) else False
    
    if request.method == 'POST' and check is not True:
        #add data to tb_pinjam
        KodePinjam = 1 if last_item is None else last_item+1
        KodeBuku = KodeBuku
        NIM = user.NIM
        TglPinjam = x.strftime("%x")
        pinjam = M_Pinjam(KodePinjam,KodeBuku,NIM,TglPinjam)
        db.session.add(pinjam)
        db.session.commit()
        print("data added!")

        #reduce stock on BUKU by 1
        buku.Stok -= 1
        db.session.merge(buku)
        db.session.commit()
        print("stock reduced!")
        return redirect(url_for('root'))
    else:
        print("Kembalikan buku!")
    return redirect(url_for('root'))

@app.route('/kembaliBuku/<KodeBuku>',methods=['GET','POST'])
def kembaliBuku(KodeBuku):
    #fetch user || USE SESSION INSTEAD
    username = 'jsmith'
    user = Anggota.query.filter_by(Username = username).first()
    
    #create date
    x = datetime.datetime.now()

    #fetch last index INT
    last_item = M_Kembali.query.order_by(M_Kembali.KodeKembali.desc()).first()
    if last_item is not None:
        last_item = last_item.KodeKembali 

    #fetch targeted row from BUKU
    buku = Buku.query.filter_by(KodeBuku=KodeBuku).first()

    if request.method == 'POST':
        #add data to tb_kembali
        KodeKembali = 1 if last_item is None else last_item+1
        KodeBuku = KodeBuku
        NIM = user.NIM
        TglKembali = x.strftime("%x")
        kembali = M_Kembali(KodeKembali,KodeBuku,NIM,TglKembali)
        db.session.add(kembali)
        db.session.commit()
        print("data added!")

        #delete row from PINJAM
        pinjam = M_Pinjam.query.filter_by(NIM=user.NIM, KodeBuku=KodeBuku).first()
        db.session.delete(pinjam)
        db.session.commit()
        print("data deleted!")

        #add stock on BUKU by 1
        buku.Stok += 1
        db.session.merge(buku)
        db.session.commit()
        print("stock added!")
        return redirect(url_for('root'))
    return redirect(url_for('root'))

#FUNCTIONALITY ANGGOTA (BELOM JALAN)
@app.route('/editAnggota/<NIM>',methods=['GET','POST'])
def editAnggota(NIM):
    form = Registration()
    data = Anggota.query.filter_by(NIM = NIM).first()

    if request.method == 'POST':
        #assign data from form to database
        data.Username = form.username.data
        data.Password = form.password.data
        db.session.merge(data)
        db.session.commit()
        return redirect(url_for('index'))
    else: 
        return render_template('editAnggota.html', form = form, data = data)

if __name__ == '__name__':
    app.run(debug=True)