from ast import If
from email import message

from distro import name
from urllib3 import request
import flask

from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)  # Fixed here

def myConn():
    return pymysql.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

@app.route("/")
def index():
    return render_template("Home.html")

@app.route("/about")
def About():
    return render_template("About.html")

@app.route("/visit")
def Visit():
    return render_template("visit.html")

@app.route("/series")
def Series():
    return render_template("Series.html")


@app.route("/photos")
def Photos():
    return render_template("Photos.html")

@app.route("/ministries")
def Ministries():
    return render_template("Ministries.html")




@app.route("/signup")
def addUsers():
     return render_template("signup.html")
 
@app.route("/signup",methods=['GET','POST'])
def receiveSignup():
     if request.method == "POST":
          fName = request.form['first_name']
          lName = request.form['last_name']
          email = request.form['email']
          password = request.form['password']
          cpassword = request.form['confirm_password']
          if password != cpassword:
               return render_template("signup.html",msg="passwords don't match")
          else:
               conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
               cur = conn.cursor()
               sql = "INSERT INTO users(f_name,l_name,email,password)VALUES(%s,%s,%s,%s)"
               cur.execute(sql,(fName,lName,email,password))
               conn.commit()
               return "<h1 style='color:green;'>User added successfully <a href='/register'>Back</a></h1>"

     else:
               return "The method is not POST"
               

@app.route("/login")
def login():
     return render_template("login.html")

@app.route("/do-login", methods=['GET','POST'])
def receiveLogin():
     if request.method == "GET":
          email = request.form['email']
          password = request.form['password']
          conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
          cur = conn.cursor()
          sql = "SELECT f_name,l_name FROM users WHERE email=%s AND password=%s"
          if cur.execute(sql,(email,password)):
               data = cur.fetchone()
               return render_template("home.html",names=data)
          else:
               return "<h1 style='color:red;'>"+email+" was not found <a href='/login' >BACK</a>"
     else:
          return "method is not POST"



@app.route("/contact")
def addContact():
    return render_template("Contact.html")

@app.route("/receive-contact",methods=['GET','POST'])
def receiveContacts():
    if request.method == "POST":
        conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
        sql = "INSERT INTO contact(name,email,phone,message)VALUES(%s,%s,%s,%s)"
        cur = conn.cursor()
        name = request.form['name']
        email =request.form['email']
        phone =request.form['phone']
        message =request.form['message']
        
       
        cur.execute(sql,(name,email,phone,message))
        conn.commit()
        return "<h1>Contacts added Successfully</h1>"
    else:
        return "The method is not POST."


@app.route("/join")
def addJoin():
    return render_template("Join.html")

@app.route("/receive-join", methods=['GET', 'POST'])
def SaveJoin():
    if request.method == "POST":
        conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
        sql = "INSERT INTO join(name,email)VALUES(%s,%s)"
        cur = conn.cursor()
        name = request.form['name']
        email = request.form['email']

        cur.execute(sql, (name, email))
        conn.commit()
        return "<h1>Join added Successfully</h1>"
    else:
        return "The method is not POST."



@app.route("/Event")
def Event():
    return render_template("Event.html")

@app.route("/receive-event", methods=['GET', 'POST'])
def receiveEvent():
    if request.method == "POST":
        fullname = request.form['fullname']
        email = request.form['email']

        conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
        cur = conn.cursor()
        sql = "INSERT INTO join(fullname,email)VALUES(%s,%s)"
        cur.execute(sql, (fullname, email))
        conn.commit()
        return "<h1>Event added Successfully</h1>"
    else:
        return "The method is not POST."


@app.route("/praise")
def Praise():
    return render_template("praise.html")

@app.route("/receive-praise", methods=['GET', 'POST'])
def receivePraise():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
        cur = conn.cursor()
        sql = "INSERT INTO join(name,email,phone,message)VALUES(%s,%s,%s,%s)"
        cur.execute(sql, (name, email, phone, message))
        conn.commit()
        return "<h1>Join added Successfully</h1>"
    else:
        return "The method is not POST."
    
    
    
@app.route("/payment")
def addPayment():
    return render_template("Payment.html")

@app.route("/receive-payment", methods=['GET', 'POST'])
def savePayment():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        amount = request.form['amount']
        comment = request.form['comment']
        conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
        cur = conn.cursor()
        sql = "INSERT INTO payment(name,email,phone,amount,comment)VALUES(%s,%s,%s,%s,%s)"
        cur.execute(sql, (name, email, phone, amount, comment))
        conn.commit()
        return "<h1>Payment Received Successfully</h1>"
    else:
        return "The method is not POST."

@app.route("/volunteer")
def addVolunteer():
    return render_template("Volunteer.html")

@app.route("/receive-volunteer", methods=['GET', 'POST'])
def saveVolunteer():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        comment = request.form['comment']
        conn = pymysql.Connect(host="localhost",user="your_username",password="your_password",database="your_database")
        cur = conn.cursor()
        sql = "INSERT INTO join(name,email,phone,comment)VALUES(%s,%s,%s,%s)"
        cur.execute(sql, (name, email, phone, comment))
        conn.commit()
        return "<h1>Join added Successfully</h1>"
    else:
        return "The method is not POST."




if __name__ == "__main__":
    
    app.run()
