from flask import render_template
from flask import request
from app import app
from app import GPIO_util
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import sys
import atexit
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from os import curdir,sep
from app import config

SITE_VERIFY_URL = config.VERIFY_URL
SECRET_KEY = config.SECRET_KEY

limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["4 per hour", "4 per hour"],
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/siteverify', methods=['POST'])
@limiter.limit("4 per hour")
def siteverify():
    body = request.json
    print(body)

@app.route('/activate', methods=['POST'])
@limiter.limit("4 per hour")
def activate():
    body = request.json
    print(body)
    RECAPTCHA_RESPONSE = body['response']

    REMOTE_IP = request.remote_addr
    params = urlencode({
        'secret':SECRET_KEY,
        'response':RECAPTCHA_RESPONSE,
    })

    data = urlopen(VERIFY_URL, params.encode('utf-8')).read()

    result = json.loads(data)
    success = result.get('success', None)

    GPIO-util.success(success, body)

def shutdown():
    GPIO-util.shutdown()

atexit.register(shutdown)
