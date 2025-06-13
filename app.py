from flask import Flask, render_template, request, redirect, url_for, Response
from functools import wraps
from config import USERNAME, PASSWORD
from datetime import datetime, timedelta
from collections import defaultdict
import os

app = Flask(__name__)

# CONFIG
MAX_FAILED_ATTEMPTS = 3
FAIL_WINDOW = timedelta(minutes=30)
BAN_DURATION = timedelta(minutes=600)

# Track attempts
failed_attempts = defaultdict(list)  # { ip: [datetime, ...] }
banned_ips = {}  # { ip: ban_expiry_datetime }

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def nauthenticate():
    from flask import Response
    return Response(
        'Could not verify your login.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr
        now = datetime.now()

        # Check if IP is banned
        if ip in banned_ips:
            if now < banned_ips[ip]:
                return Response("Too many failed attempts. Try again later.", 429)
            else:
                # Ban expired
                banned_ips.pop(ip)

        auth = request.authorization

        # Validate credentials
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            # Clean old attempts
            failed_attempts[ip] = [t for t in failed_attempts[ip] if now - t < FAIL_WINDOW]
            failed_attempts[ip].append(now)

            if len(failed_attempts[ip]) >= MAX_FAILED_ATTEMPTS:
                banned_ips[ip] = now + BAN_DURATION
                failed_attempts.pop(ip, None)
                return Response("Too many failed attempts. You are temporarily blocked.", 429)

            return Response("Invalid credentials", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

        # On success: reset attempt history
        failed_attempts.pop(ip, None)
        return f(*args, **kwargs)

    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

@app.route('/restart', methods=['POST'])
@requires_auth
def restart():
    os.system("shutdown /r /t 0")
    return "Restarting system..."

@app.route('/favicon.ico')
@requires_auth
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8116)
