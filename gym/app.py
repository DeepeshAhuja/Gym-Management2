from flask import Flask, render_template, request, redirect,session,flash
from flask_mysqldb import MySQLdb,MySQL
import MySQLdb.cursors
from flask_session import Session
from flask_mail import Mail, Message

app= Flask(__name__)
app.secret_key = 'abcdefg123'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root123$'
app.config['MYSQL_DB']='login'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/profile')
def profile():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select first_name,last_name,address,gender,email,mobile,workouts,billing_no,billing_date,batch,mem_category,reg_date,sub_status,reg_fee from members where email='{}';".format(session['email'])) 
    mysql.connection.commit()
    user=cursor.fetchone()
    return render_template("profile.html",user=user)

@app.route('/membership', methods=['POST','GET'])
def membership():
    if request.method=='POST' :
        first_name=request.form.get('fname')
        last_name=request.form.get('lname')
        address=request.form.get('address')
        email=request.form.get('email')
        phone=request.form.get('phone')
        gender=request.form.get('gender')
        workouts=request.form.get('workout')
        membership=request.form.get('membership')
        billingno= request.form.get('Billing No')
        billdate=request.form.get('Billing date')
        batchmem= request.form.get('Batch Membership')
        regdate=request.form.get('Register date')
        status= request.form.get("status") 
        regfees=request.form.get("Registration Fees")
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO members (first_name,last_name,address,gender,email,mobile,workouts,billing_no,billing_date,batch,mem_category,reg_date,sub_status,reg_fee) VALUES ('{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}',{});".format(first_name, last_name,address,gender,email,phone,workouts,billingno,billdate,batchmem,membership,regdate,status,regfees))
        mysql.connection.commit()
        # user=cursor.fetchone()
    return render_template("membership.html")

@app.route('/attendance',methods=['POST','GET'])
def attendance():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select id from members where email='{}';".format(session['email'])) 
    mysql.connection.commit()
    user=cursor.fetchone()
    return render_template("attendance.html",user=user)

@app.route('/login',methods=['GET','POST'])
def login():
    message=''
    if request.method=="POST" and request.form['email'] and request.form['password']:
        password=request.form['password']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_login WHERE email = '{}' AND password = '{}';".format(email,password))
        user=cursor.fetchone()
        if user:
            session["email"] = request.form.get("email")
            flash('Logged in successfully')
            return redirect("/")
        else:
            message='Enter proper credentials'   
    return render_template('login.html',message=message)

@app.route('/signup',methods=['GET','POSt'])
def signup():
    if request.method=="POST" and request.form['username'] and request.form['email'] and request.form['password']:
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO user_login (name,email,password) VALUES ('{}', '{}', '{}');".format(username, email, password))
        user=cursor.fetchone()
        mysql.connection.commit()
        if user:
            return redirect('/login')
    return render_template('signup.html')

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    message=''
    if request.method=="POST" and request.form['email'] and request.form['password']:
        password=request.form['password']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM admin_login WHERE email = '{}' AND password = '{}';".format(email,password))
        user=cursor.fetchone()
        if user:
            session["email"] = request.form.get("email")
            flash('Logged in successfully')
            return redirect("/")
        else:
            message='Enter proper credentials'   
    return render_template('login.html',message=message)

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True,port=8000)