from flask import Flask, render_template, request, redirect,session,flash
from flask_mysqldb import MySQLdb,MySQL
import MySQLdb.cursors
from flask_session import Session
from flask_mail import Mail, Message

app= Flask(__name__)
app.secret_key = 'xyz123abc'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root123$'
app.config['MYSQL_DB']=''

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

if __in