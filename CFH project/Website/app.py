from flask import Flask,render_template,request,redirect 
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

app = Flask(__name__)

#make a global variable for our connection instead of a function 
conn = pymysql.connect(host="localhost",user="root",database="")


@app.route("/Mpesa", methods=['GET', 'POST'])
def mpesa():
    if request.method == "POST":
        amount = request.form["amount"]
        phone = request.form["phone"]
        # MPESA STK PUSH PROCESS (Sim Toolkit Push)
        # 1. GENERATING THE ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
        # 2. GET THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "4516972"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
        # 3. SETUP THE PAYLOAD (All the info we need to send to Safaricom)
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
        return "The method is not POST.Do not access this route directly"
    
@app.route('/paypal', methods=['POST'])
def paypal():
    if request.method == "POST":
        amount = request.form["amount"]
        # Create a new payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "",
                "cancel_url": ""
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
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "Donation to CFH Chapel"
            }]
        })

        if payment.create():
            print("Payment created successfully")
            # Redirect the user to PayPal for approval
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            print(payment.error)
            return "An error occurred while creating the payment."
    else:
        return "The method is not POST. Do not access this route directly."

@app.route('/Mastercard', methods=['POST'])
def mastercard():
    if request.method == "POST":
        amount = request.form["amount"]
        # Initialize the Mastercard client
        client = MastercardClient(
        consumer_key='your_consumer_key',
        private_key='path_to_your_private_key.pem',
        environment='sandbox'  # Use 'production' for live transactions
        )

        # Create a payment request
        payment_request = PaymentRequest(
        amount=amount,
        currency='USD',
        card_number='4111111111111111',  # Test card number
        card_expiry_month='12',
        card_expiry_year='2025',
        card_cvv='123',
        description='Donation to CFH Chapel'
        )

        # Process the payment
        response = client.payments.create(payment_request)

        if response.status == 'APPROVED':
            return "Payment processed successfully."
        else:
            return f"Payment failed: {response.error_message}"
    else:
        return "The method is not POST. Do not access this route directly."
   
    
if __name__ == "__main__": 
    app.run(debug=True)
