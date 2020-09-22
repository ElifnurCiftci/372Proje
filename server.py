import os
from db_init import initialize

from flask import Flask, redirect, url_for, render_template, request, Blueprint

from psycopg2 import extensions
from queries import *

from views.actor import actor
from views.movie import movie

extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask(__name__)

app.register_blueprint(actor,url_prefix="/actors")
app.register_blueprint(movie,url_prefix="/movies")

HEROKU = True

if(not HEROKU): 
    os.environ['DATABASE_URL'] = "dbname='postgres' user='postgres' host='localhost' password='1234'"
    initialize(os.environ.get('DATABASE_URL'))

@app.route("/")
def home_page():
    return render_template("home_page.html")

if __name__ == "__main__":
    if(not HEROKU):
        app.run(debug = True)
    else:
        app.run()