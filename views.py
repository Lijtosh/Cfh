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

    
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"  

if __name__ == '__main__':
    app.run(debug=True)