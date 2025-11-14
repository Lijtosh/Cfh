from ast import If
from email import message
import json
import re

from distro import name
from urllib3 import request
import flask

from flask import Flask, render_template, request
import pymysql
import os #for dealing with the operating system folders 
from werkzeug.utils import secure_filename #pulling filename from a file 
import requests #installation: pip3 install requests
from requests.auth import HTTPBasicAuth
import datetime
import base64
import paypalrestsdk
from flask import Flask, request, render_template
from mastercard_sdk import MastercardClient, PaymentRequest
from Website.Test import Children, receiveEvent


app = Flask(__name__)  



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

@app.route("/contact")
def addContact():
    return render_template("Contact.html")

@app.route("/receive-contact", methods=['GET','POST'])
def receiveContacts():
    try:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        conn, cur = get_db_connection()
        sql = "INSERT INTO contact(name,email,subject,message) VALUES (%s,%s,%s,%s)"
        cur.execute(sql, (name, email, subject, message))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/Contact.html")
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/register-prayerRequest', methods=['GET','POST'])
def register_prayerRequest():
    if request.method == "POST":
        name = request.form["name"]
        prayerRequest = request.form["prayerRequest"]
        conn,cur = get_db_connection()
        conn = pymysql.connect(host="localhost",user="username",password="password",database="database")
        cur = conn.cursor
        sql = "INSERT INTO prayerRequest(name,prayerRequest)VALUES(%s,%s)"
        cur.execute(sql, (name, prayerRequest))
        conn.commit()
        return redirect("/Contact.html")
    else:
        return "method is not POST"
    
@app.route("/mizizi")
def Mizizi():
    return render_template("Mizizi.html")
    
@app.route('/register-submission', methods=['GET','POST'])
def register_submission():
    data = request.form.to_dict()
    required_fields = ['firstName', 'lastName', 'email', 'phone', 'church', 'privacyCheck']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False,'message': 'Error: Missing required fields.'}), 400
    try:
        conn, cur = get_db_connection()
        sql = "INSERT INTO mizizi_registrations(first_name, last_name, email, phone, location, is_cfh_member, motivation, agreed_to_contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql, (
            data.get('firstName'),
            data.get('lastName'),
            data.get('email'),
            data.get('phone'),
            data.get('location', 'N/A'),
            data.get('church'),
            data.get('motivation', ''),
            bool(data.get('privacyCheck'))
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': f"Registration successful for {data.get('firstName')}!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route("/ministries")
def Ministries():
    return render_template("Ministries.html")

@app.route("/receive-ministry", methods=['GET','POST'])
def receiveMinistry():
    data = request.form.to_dict()
    required_fields = ['name', 'email', 'ministry', 'comment']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False,'message': 'Error: Missing required fields.'}), 400
    try:
        conn, cur = get_db_connection()
        sql = "INSERT INTO ministry_register(name,email,ministry,comment) VALUES (%s,%s,%s,%s)"
        cur.execute(sql, (
            data.get('name'),
            data.get('email'),
            data.get('ministry'),
            data.get('comment')
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': f"Ministry registration successful for {data.get('name')}!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/receive-event", methods=['GET','POST'])
def receiveEvent():
    data = request.form.to_dict()
    required_fields = ['name', 'email', 'event', 'question']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False,'message': 'Error: Missing required fields.'}), 400
    try:
        conn, cur = get_db_connection()
        sql = "INSERT INTO event(name,email,event,question) VALUES (%s,%s,%s,%s)"
        cur.execute(sql, (
            data.get('name'),
            data.get('email'),
            data.get('event'),
            data.get('question')
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': f"Event registration successful for {data.get('name')}!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/receive-children", methods=['GET','POST'])
def receiveChildren():
    data = request.form.to_dict()
    required_fields = ['name', 'email', 'ministry']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False,'message': 'Error: Missing required fields.'}), 400
    try:
        conn, cur = get_db_connection()
        sql = "INSERT INTO children(name,email,ministry) VALUES (%s,%s,%s)"
        cur.execute(sql, (
            data.get('name'),
            data.get('email'),
            data.get('ministry')
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': f"Children registration successful for {data.get('name')}!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/register")
def register():
    return render_template("Register.html")

@app.route("/receive-kid", methods=['GET','POST'])
def receiveKid():
    try:
        name = request.form['name']
        age = request.form['age']
        parentName = request.form['parentName']
        parentPhone = request.form['parentPhone']
        parentEmail = request.form['parentEmail']
        conn, cur = get_db_connection()
        sql = """
        INSERT INTO register_kid(name,age,parentName,parentPhone,parentEmail) 
        VALUES(%s,%s,%s,%s,%s)
        """
        cur.execute(sql, (name, age, parentName, parentPhone, parentEmail))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': f"Kid registration successful for {name}!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/join")
def addJoin():
    return render_template("Join.html")

@app.route("/receive-join") 
def receiveJoin(): 
    data = request.form.to_dict()
    required_fields = ['name', 'email', 'ministry','gift']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False,'message': 'Error: Missing required fields.'}), 400
    try:
        conn, cur = get_db_connection()
        sql = "INSERT INTO join(name,email,ministry,gift) VALUES (%s,%s,%s,%s)"
        cur.execute(sql, (
            data.get('name'),
            data.get('email'),
            data.get('ministry')
            data.get('gift')
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': f"Join registration successful for {data.get('name')}!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/payment")
def addPayment():
    return render_template("Payment.html")

@app.route("/mpesa", methods=['GET','POST'])
def mpesa():
    if request.method == "POST":
        amount = request.form["amount"]
        phone = request.form["phone"]
        #MPESA STK PUSH PROCESS (Sim Toolkit Push)
        #1. GENERATING THE ACESS TOKEN 
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
        #2. GET THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "4516972"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
        #3. SETUP THE PAYLOAD (All the info we need to send to safaricom)
        payload = {
                    "BusinessShortCode": "4516972",
                    "Password": "{}".format(password),
                    "Timestamp": "{}".format(timestamp),
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": amount,  # use 1 when testing
                    "PartyA": phone,  # change to your number
                    "PartyB": "4516972",
                    "PhoneNumber": phone,
                    "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                    "AccountReference": "account",
                    "TransactionDesc": "account"
            }
        #4. POPULATE THE HTTP HEADER
        headers = {
                    "Authorization": access_token,
                    "Content-Type": "application/json"
        }
        #5. SEND THE REQUEST (Send all the above to initiate an STK push)
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL
        response = requests.post(url, json=payload, headers=headers)
        print (response.text)
        return render_template("payment.html",phone = phone,amount = amount)
    else:
        return "The method is not POST.Do not acess this route directly"

@app.route('/paypal', methods=['GET','POST'])
def paypal():
    if request.method == "POST":
        amount = request.form.get("amount")
        paypalrestsdk.configure({
            "mode": "sandbox", # or "live"
            "client_id": os.getenv("PAYPAL_CLIENT_ID"),
            "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "https://yourdomain.com/paypal/success",
                "cancel_url": "https://yourdomain.com/paypal/cancel"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Donation",
                        "sku": "donation",
                        "price": amount,
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {"total": amount, "currency": "USD"},
                "description": "Donation to CFH Chapel"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
            return "Approval URL not found", 500
        else:
            return f"An error occurred: {payment.error}", 400
    return "Invalid request method", 405

@app.route('/Mastercard', methods=['GET','POST'])
def mastercard():
    if request.method == "POST":
        amount = request.form.get("amount")
        # Initialize Mastercard client with credentials from environment variables
        client = MastercardClient(
            consumer_key=os.getenv('MASTERCARD_CONSUMER_KEY'),
            private_key=os.getenv('MASTERCARD_PRIVATE_KEY_PATH'),
            environment='sandbox'
        )
        payment_request = PaymentRequest(
            amount=amount,
            currency='USD',
            card_number='4111111111111111',
            card_expiry_month='12',
            card_expiry_year='2025',
            card_cvv='123',
            description='Donation to CFH Chapel'
        )
        response = client.payments.create(payment_request)
        if response.status == 'APPROVED':
            return "Payment processed successfully."
        else:
            return f"Payment failed: {response.error_message}"
    return "Invalid request method", 405
    

def myConn():
    return pymysql.connect(host='localhost',user='root',database='oreo_elijah_admin')


if __name__ == "app.py":
    
    app.run(debug=True)
    


