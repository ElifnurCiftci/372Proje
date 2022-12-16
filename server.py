import os
from db_init import initialize
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session,redirect, url_for, render_template, request, Blueprint, flash
import psycopg2
import psycopg2.extras
from psycopg2 import extensions
from queries import *
from generalFuncs import *
from views.eczane import eczane
import re
import random


extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask(__name__)
app.secret_key='my super secret key'.encode('utf8')

app.register_blueprint(eczane,url_prefix="/eczane")

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
    role = session['role']
    #return session['role'] + ' olarak giriş yapıldı.<br>' +"Hoşgeldin "+ username + '!<br>'+ "<b><a href = '/eczane'>Eczaneleri Listele</a></b><br><b><a href = '/logout'>Çıkış yapmak içi tıkla</a></b>" 
    return render_template("home_page.html", role=role, username=username)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form:
        username = request.form['username']
        print(username)
        if(username.lower() == "ziyaretci" or username.lower() == "ziyaretçi"):
            session['loggedin'] = True
            session['role'] = "Ziyaretçi"
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
                print(password_rs)
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
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            id = str(random.randint(10000,99999));
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

if __name__ == "__main__":
    if(not HEROKU):
        app.run(debug = True)
    else:
        app.run()