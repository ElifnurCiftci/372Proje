import os
from db_init import initialize

from flask import Flask, session,redirect, url_for, render_template, request, Blueprint

from psycopg2 import extensions
from queries import *
from generalFuncs import *
from views.eczane import eczane


extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask(__name__)
app.secret_key='my super secret key'.encode('utf8')

app.register_blueprint(eczane,url_prefix="/eczane")

HEROKU = False

if(not HEROKU): 
    os.environ['DATABASE_URL'] = "dbname='proje_yeni' user='postgres' host='localhost' password='2108'"
    initialize(os.environ.get('DATABASE_URL'))

@app.route("/")
def index():
    userid=""
    if session.__contains__('userid'):
        userid = ""+session['userid']
        userrole, username = whatRole(userid)
        return userrole + ' olarak giriş yapıldı.<br>' +"Hoşgeldin "+ username + '!<br>'+ "<b><a href = '/eczane'>Eczaneleri Listele</a></b><br><b><a href = '/logout'>Çıkış yapmak içi tıkla</a></b>" 
    return render_template("home_page.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if "login" in request.form:
            kullanıcı = select("kullanıcı_id","kullanici",asDict=True)
            for kullanıcı in kullanıcı:
                if(kullanıcı['kullanıcı_id']==request.form.get('userid')):
                    userid = kullanıcı['kullanıcı_id']
                    session['userid'] = userid 
                    userrole, username = whatRole(userid)
                    sifre=""
                    if(userrole=="uye"):
                        uye = select("uye_sifre", "uye","kullanıcı_id='{}'".format(userid),asDict=True)
                        sifre = uye['uye_sifre']
                    if(userrole=="admin"):
                        admin = select("admin_sifre", "admin","kullanıcı_id='{}'".format(userid),asDict=True)
                        sifre = admin['admin_sifre']
                    if(sifre==request.form.get('psw') or userrole=="ziyaretci"):
                        return redirect(url_for('index'))
    return render_template("login_page.html")

@app.route('/logout')
def logout():
   # remove the userid from the session if it is there
   session.pop('userid', None)
   return redirect(url_for('login'))

if __name__ == "__main__":
    if(not HEROKU):
        app.run(debug = True)
    else:
        app.run()