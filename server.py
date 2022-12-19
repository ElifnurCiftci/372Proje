import os
from db_init import initialize
from flask import Flask, session,redirect, url_for, render_template, request, Blueprint, flash
import psycopg2
import psycopg2.extras
from psycopg2 import extensions
from queries import *
from generalFuncs import *
import re
import random
from datetime import datetime


extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask(__name__)
app.secret_key='my super secret key'.encode('utf8')


HEROKU = False

if(not HEROKU): 
    os.environ['DATABASE_URL'] = "dbname='proje_yeni' user='postgres' host='localhost' password='2108'"
    initialize(os.environ.get('DATABASE_URL'))

DB_HOST = "localhost"
DB_NAME = "proje_yeni"
DB_USER = "postgres"
DB_PASS = "2108"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route("/")
def home():
    username = session['username'] if session.__contains__('username') else ""
    role = session['role'] if session.__contains__('role') else ""
    #return session['role'] + ' olarak giriş yapıldı.<br>' +"Hoşgeldin "+ username + '!<br>'+ "<b><a href = '/eczane'>Eczaneleri Listele</a></b><br><b><a href = '/logout'>Çıkış yapmak içi tıkla</a></b>" 
    return render_template("home_page.html", role=role, username=username)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form:
        username = request.form['username']
        if(username.lower() == "ziyaretci" or username.lower() == "ziyaretçi"):
            session['loggedin'] = True
            session['role'] = "ziyaretci"
            return redirect(url_for('home'))
        elif 'password' in request.form:
            password = request.form['password']
            sifre_holder="uye_sifre"
            isim_holder="uye_ad"
            # Check if account exists using MySQL
            cursor.execute('SELECT * FROM uye WHERE uye_ad = %s', (username,))
            
            # Fetch one record and return result
            account = cursor.fetchone()
            if not account:
                cursor.execute('SELECT * FROM admin WHERE admin_ad = %s', (username,))
                account = cursor.fetchone()
                sifre_holder="admin_sifre"
                isim_holder="admin_ad"
    
            if account:
                password_rs = account[sifre_holder]
                # If account exists in users table in out database
                if (password_rs == password):
                    # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['id'] = account['kullanıcı_id']
                    session['role'] = whatRole(username)
                    session['username'] = account[isim_holder]
                    # Redirect to home page
                    return redirect(url_for('home'))
                else:
                    # Account doesnt exist or username/password incorrect
                    flash('Incorrect username/password')
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
 
    return render_template('login_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username'].strip()
        password = request.form['password'].strip()
    
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM uye WHERE uye_ad = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            id = str(random.randint(10000,99999))
            cursor.execute("INSERT INTO kullanici (kullanıcı_id) VALUES (%s)", (id,))
            cursor.execute("INSERT INTO uye (uye_ad, uye_sifre, kullanıcı_id) VALUES (%s,%s,%s)", (username, password, id))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')

@app.route('/logout')
def logout():
   # remove the userid from the session if it is there
   session.pop('username', None)
   session.pop('id', None)
   session.pop('role', None)
   session.pop('loggedin', None)
   return redirect(url_for('login'))

@app.route('/siparis', methods=['GET', 'POST'])
def siparis():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'GET':
        if session['role']=="admin":
            cursor.execute("SELECT kullanıcı_id, siparis.siparis_id,ilac_adi,ilac_id,ilac_cesidi,siparis_tarihi FROM siparis left JOIN ilac ON ilac.siparis_id=siparis.siparis_id")
        else:
            cursor.execute("SELECT siparis.siparis_id,ilac_adi,ilac_id,ilac_cesidi,siparis_tarihi FROM siparis left JOIN ilac ON ilac.siparis_id=siparis.siparis_id WHERE kullanıcı_id='"+(session['id'])+"'")
        siparis2=cursor.fetchall()
        conn.commit()
        return render_template("siparis.html", siparis=siparis2, role=session['role'])
    elif request.method == "POST":
        if "sepetten_cıkar" in request.form:
            id = str(random.randint(1000000000,9999999999))
            siparis = request.form.get('sepetten_cıkar')
            siparis =re.sub('[\[\]]', '',siparis)
            siparis =re.sub(' +', '',siparis)
            siparis = siparis.split(",")
            siparis_id = siparis[1] if session['role'] == "admin" else siparis[0]
            ilac_id = siparis[4] if session['role'] == "admin" else siparis[3]
            cursor.execute("DELETE FROM siparis WHERE siparis_id="+siparis_id)
            if ilac_id != "none" and ilac_id != "None":
                cursor.execute ("UPDATE ilac SET siparis_id=null WHERE ilac_id="+ilac_id)
            conn.commit()
        return redirect(url_for("siparis"))


@app.route("/ilac/", methods=['GET','POST'])
def ilac():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == "GET":    
        ilac = select("ilac_adi,ilac_cesidi,ilac_id,son_kullanma_tarihi","ilac","siparis_id is null order by son_kullanma_tarihi desc",asDict=True)
        return render_template("ilac.html", ilac = ilac, eczane_ad="Tüm", role=session['role'])
    elif request.method == "POST":
        if "sepete_ekle" in request.form:
            id = str(random.randint(1000000000,9999999999))
            ilac_id = "'"+request.form.get('sepete_ekle')+"'"
            cursor.execute("INSERT INTO siparis (siparis_id,kullanıcı_id,siparis_tarihi) VALUES (%s,%s,%s)", (id,session['id'],datetime.today().strftime('%Y-%m-%d')))
            cursor.execute ("UPDATE ilac SET siparis_id='"+id+"' WHERE ilac_id="+ilac_id)
            conn.commit()
        elif "ara" in request.form:
            ilac_ad = "'"+str(request.form.get('aranan')).lower()+"'"
            cursor.execute("SELECT ilac_adi,ilac_cesidi,ilac_id,son_kullanma_tarihi FROM ilac WHERE siparis_id is null and LOWER(ilac_adi)="+ilac_ad+" order by son_kullanma_tarihi desc")
            ilac = cursor.fetchall()
            conn.commit()
            return render_template("ilac.html", ilac = ilac, eczane_ad="Tüm", role=session['role'])
        return redirect(url_for("ilac"))

@app.route("/eczane/", methods=['GET','POST'])
def eczane_page():
    if request.method == "GET":
        eczane = select("eczane_ad,eczane_id,eczane_adres,eczane_tel_no,eczane_e_posta","eczane",asDict=True)
        return render_template("eczane.html", eczane = eczane)

@app.route("/eczane/<eczane_id>", methods=['GET','POST'])
def eczane_detail_page(eczane_id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    eczane_ad = select("eczane_ad","eczane","eczane_id='{}'".format(eczane_id),asDict=True)
    if request.method == "GET":
        ilac = select("ilac_adi,ilac_id,ilac_cesidi,son_kullanma_tarihi","ilac natural join anlasma_saglar","eczane_id='{}' and siparis_id is null order by son_kullanma_tarihi desc".format(eczane_id),asDict=True)
        return render_template("ilac.html", ilac = ilac, eczane_ad=eczane_ad['eczane_ad']+" Eczanesindeki", role=session['role'])
    elif request.method == "POST":
        if "sepete_ekle" in request.form:
            id = str(random.randint(1000000000,9999999999))
            ilac_id = "'"+request.form.get('sepete_ekle')+"'"
            cursor.execute("INSERT INTO siparis (siparis_id,kullanıcı_id,siparis_tarihi) VALUES (%s,%s,%s)", (id,session['id'],datetime.today().strftime('%Y-%m-%d')))
            cursor.execute ("UPDATE ilac SET siparis_id='"+id+"' WHERE ilac_id="+ilac_id)
            conn.commit()
        elif "ara" in request.form:
            ilac_ad = str(request.form.get('aranan')).lower()
            ilac = select("ilac_adi,ilac_id,ilac_cesidi,son_kullanma_tarihi","ilac natural join anlasma_saglar","eczane_id='{}'".format(eczane_id)+"and LOWER(ilac_adi)='{}' and siparis_id is null order by son_kullanma_tarihi desc".format(ilac_ad),asDict=True)
            return render_template("ilac.html", ilac = ilac, eczane_ad=eczane_ad['eczane_ad']+" Eczanesindeki", role=session['role'])
        return redirect(url_for('eczane_detail_page', eczane_id=eczane_id))
if __name__ == "__main__":
    if(not HEROKU):
        app.run(debug = True)
    else:
        app.run()