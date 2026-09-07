"""
==============================================================================
QUESTION 34: Flask JWT Authentication with Flask-Limiter
==============================================================================
Description:
Flask web application with `@token_required` decorator for JWT validation 
and `@limiter.limit("5 per minute")` for brute-force login protection.
==============================================================================
"""
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import jwt
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
SECRET_KEY = "my_flask_jwt_secret_key_12345"

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"]
)

USER_DB = {"admin": "SecurePassword123!"}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"status": "error", "message": "Token is missing"}), 401
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_data = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"status": "error", "message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status": "error", "message": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if USER_DB.get(username) == password:
        now = datetime.now(timezone.utc)
        payload = {"sub": username, "iat": now, "exp": now + timedelta(minutes=10)}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"status": "success", "token": token}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({"status": "success", "user": request.user_data}), 200

if __name__ == '__main__':
    print("=== QUESTION 34: FLASK JWT AUTHENTICATION WITH RATE LIMITER ===")
    app.run(port=5000, debug=True)
